import re

# PHP unserialize equivalent

__all__ = ['unserialize','unserialize_file']

class ParseError(Exception):
        def __init__(self, msg):
                self.msg = msg

        def __str__(self):
                return 'ParseError: %s' % self.msg

def p_sep(text):
        if text[0] == ':':
                return text[1:], (':',)
        else:
                raise ParseError(text)

def p_sep2(text):
        if text[0] == ';':
                return text[1:], (';',)
        else:
                raise ParseError(text)

def p_int(text):
        text, t = p_sep(text)
        text, i = p_num(text)
        return [text, i]

def p_num(text):
        m = num_re.match(text)
        if not m:
                raise ParseError(text)
        else:
                return text[m.end():], int(m.group(1))

def p_str(text):
        text, tokens = p_sep(text)
        text, strlen = p_num(text)
        strlen += 2
        text, tokens = p_sep(text)
        this_str = text[1:strlen-1]
        return text[strlen:], this_str

def p_bool(text):
        text, t = p_sep(text)
        text, i = p_num(text)
        return [text, i and True or False]

def p_null(text):
	return [text, None]

def p_arr(text):
	text, t = p_sep(text)
	text, arrlen = p_num(text)
	text, t = p_sep(text)
	
	# start array
	if text[0] != '{':
		raise ParseError(text)
	text = text[1:]
	arr = {}
	for x in xrange(arrlen):
		text, key = unserialize(text)
		if not isinstance(key, dict):
			text, t = p_sep2(text)
		
		text, value = unserialize(text)
		if not isinstance(value, dict):
			text, t = p_sep2(text)
		
		arr[key] = value
	
	if text[0] != '}':
		raise ParseError(text)
	text = text[1:]
	
	return text, arr

def p_obj(text):
	text, key = p_str(text)
	text, value = p_arr(text)
	return [text, {key:value}]

type_dict = {
	'O': p_obj,
	's': p_str,
	'a': p_arr,
	'N': p_null,
	'i': p_int,
	'b': p_bool,
	}

num_re = re.compile('^(\d+)')
type_re = re.compile('^(%s)' % '|'.join(type_dict.keys()))
separator_re = re.compile('^(:)')
string_re = re.compile('^"(\w+)"')

def unserialize(text):
	m = type_re.match(text)
	type = m.group(1)
	return type_dict.get(type)(text[m.end():])

def unserialize_file(f):
	d = open(f).read()
	return unserialize(d)

def test():
	text, s = p_str(':10:"to je test"')
	assert(['', 'to je test'] == [text, s])
	text, a = p_arr(':2:{s:4:"name";s:0:"";s:5:"value";s:0:"";}')
	assert(['', {'name': '', 'value': ''}] == [text, a])

if __name__ == "__main__":
	import sys
	from pprint import pprint
	if len(sys.argv) > 1:
		print '='*60
		pprint (unserialize_file(sys.argv[1]))
	else:
		test()

