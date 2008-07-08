"""
MediaWiki-style markup
parse(text) -- returns safe-html from wiki markup
code based off of mediawiki

should be noted that this code is taken straight from http://www.djangosnippets.org/snippets/139/
"""

import re, random, math, locale
from base64 import b64encode, b64decode

mTagHooks = {}

def registerTagHook(tag, function):
	mTagHooks[tag] = function

def removeHtmlComments(text):
	"""remove <!-- text --> comments from given text"""
	sb = []
	start = text.find(u'<!--')
	last = 0
	while start != -1:
		end = text.find(u'-->', start)
		if end == -1:
			break
		end += 3	
		
		spaceStart = max(0, start-1)
		spaceEnd = end
		while text[spaceStart] == u' ' and spaceStart > 0:
			spaceStart -= 1
		while text[spaceEnd] == u' ':
			spaceEnd += 1
		
		if text[spaceStart] == u'\n' and text[spaceEnd] == u'\n':
			sb.append(text[last:spaceStart])
			sb.append(u'\n')
			last = spaceEnd+1
		else:
			sb.append(text[last:spaceStart+1])
			last = spaceEnd
		
		start = text.find(u'<!--', end)
	sb.append(text[last:])
	return u''.join(sb)

_attributePat = re.compile(ur'''(?:^|\s)([A-Za-z0-9]+)(?:\s*=\s*(?:"([^<"]*)"|'([^<']*)'|([a-zA-Z0-9!#$%&()*,\-./:;<>?@[\]^_`{|}~]+)|#([0-9a-fA-F]+)))''', re.UNICODE)
_space = re.compile(ur'\s+', re.UNICODE)

def decodeTagAttributes(text):
	"""docstring for decodeTagAttributes"""
	attribs = {}
	if text.strip() == u'':
		return attribs
	scanner = _attributePat.scanner(text)
	match = scanner.search()
	while match:
		key, val1, val2, val3, val4 = match.groups()
		value = val1 or val2 or val3 or val4
		if value:
			value = _space.sub(u' ', value).strip()
		else:
			value = ''
		attribs[key] = decodeCharReferences(value)
		
		match = scanner.search()
	return attribs

def setupAttributeWhitelist():
	common = ( u'id', u'class', u'lang', u'dir', u'title', u'style' )
	block = common + (u'align',)
	tablealign = ( u'align', u'char', u'charoff', u'valign' )
	tablecell = ( u'abbr',
					u'axis',
					u'headers',
					u'scope',
					u'rowspan',
					u'colspan',
					u'nowrap', # deprecated
					u'width',  # deprecated
					u'height', # deprecated
					u'bgcolor' # deprecated
					)
	return {
		u'div':			block,
		u'center':		common, # deprecated
		u'span':		block, # ??
		u'h1':			block,
		u'h2':			block,
		u'h3':			block,
		u'h4':			block,
		u'h5':			block,
		u'h6':			block,
		u'em':			common,
		u'strong':		common,
		u'cite':		common,
		u'code':		common,
		u'var':			common,
		u'img':			common + (u'src', u'alt', u'width', u'height',),
		u'blockquote':	common + (u'cite',),
		u'sub':			common,
		u'sup':			common,
		u'p':			block,
		u'br':			(u'id', u'class', u'title', u'style', u'clear',),
		u'pre':			common + (u'width',),
		u'ins':			common + (u'cite', u'datetime'),
		u'del':			common + (u'cite', u'datetime'),
		u'ul':			common + (u'type',),
		u'ol':			common + (u'type', u'start'),
		u'li':			common + (u'type', u'value'),
		u'dl':			common,
		u'dd':			common,
		u'dt':			common,
		u'table':		common + ( u'summary', u'width', u'border', u'frame',
									u'rules', u'cellspacing', u'cellpadding',
									u'align', u'bgcolor',
							),
		u'caption':		common + (u'align',),
		u'thead':		common + tablealign,
		u'tfoot':		common + tablealign,
		u'tbody':		common + tablealign,
		u'colgroup':	common + ( u'span', u'width' ) + tablealign,
		u'col':			common + ( u'span', u'width' ) + tablealign,
		u'tr':			common + ( u'bgcolor', ) + tablealign,
		u'td':			common + tablecell + tablealign,
		u'th':			common + tablecell + tablealign,
		u'tt':			common,
		u'b':			common,
		u'i':			common,
		u'big':			common,
		u'small':		common,
		u'strike':		common,
		u's':			common,
		u'u':			common,
		u'font':		common + ( u'size', u'color', u'face' ),
		u'hr':			common + ( u'noshade', u'size', u'width' ),
		u'ruby':		common,
		u'rb':			common,
		u'rt':			common, #array_merge( $common, array( 'rbspan' ) ),
		u'rp':			common,
	}
_whitelist = setupAttributeWhitelist()

def validateTagAttributes(attribs, element):
	"""docstring for validateTagAttributes"""
	out = {}
	if element not in _whitelist:
		return out
	whitelist = _whitelist[element]
	for attribute in attribs:
		value = attribs[attribute]
		if attribute not in whitelist:
			continue
		# Strip javascript "expression" from stylesheets.
		# http://msdn.microsoft.com/workshop/author/dhtml/overview/recalc.asp
		if attribute == u'style':
			value = checkCss(value)
			if value == False:
				continue
		elif attribute == u'id':
			value = escapeId(value)
		# If this attribute was previously set, override it.
		# Output should only have one attribute of each name.
		out[attribute] = value
	return out

def safeEncodeAttribute(encValue):
	"""docstring for safeEncodeAttribute"""
	encValue = encValue.replace(u'&', u'&amp;')
	encValue = encValue.replace(u'<', u'&lt;')
	encValue = encValue.replace(u'>', u'&gt;')
	encValue = encValue.replace(u'"', u'&quot;')
	encValue = encValue.replace(u'{', u'&#123;')
	encValue = encValue.replace(u'[', u'&#91;')
	encValue = encValue.replace(u"''", u'&#39;&#39;')
	encValue = encValue.replace(u'ISBN', u'&#73;SBN')
	encValue = encValue.replace(u'RFC', u'&#82;FC')
	encValue = encValue.replace(u'PMID', u'&#80;MID')
	encValue = encValue.replace(u'|', u'&#124;')
	encValue = encValue.replace(u'__', u'&#95;_')
	encValue = encValue.replace(u'\n', u'&#10;')
	encValue = encValue.replace(u'\r', u'&#13;')
	encValue = encValue.replace(u'\t', u'&#9;')
	return encValue

def fixTagAttributes(text, element):
	if text.strip() == u'':
		return u''
	
	stripped = validateTagAttributes(decodeTagAttributes(text), element)
	
	sb = []
	
	for attribute in stripped:
		value = stripped[attribute]
		encAttribute = attribute.replace(u'&', u'&amp;').replace(u'<', u'&lt;').replace(u'>', u'&gt;')
		encValue = safeEncodeAttribute(value)
		
		sb.append(u' ')
		sb.append(encAttribute)
		sb.append(u'="')
		sb.append(encValue)
		sb.append(u'"')
	
	return u''.join(sb)

_tagPattern = re.compile(ur'^(/?)(\w+)([^>]*?)(/?>)([^<]*)$', re.UNICODE)	

_htmlpairs = ( # Tags that must be closed
	u'b', u'del', u'i', u'ins', u'u', u'font', u'big', u'small', u'sub', u'sup', u'h1',
	u'h2', u'h3', u'h4', u'h5', u'h6', u'cite', u'code', u'em', u's',
	u'strike', u'strong', u'tt', u'var', u'div', u'center',
	u'blockquote', u'ol', u'ul', u'dl', u'table', u'caption', u'pre',
	u'ruby', u'rt' , u'rb' , u'rp', u'p', u'span', u'u'
)
_htmlsingle = (
	u'br', u'hr', u'li', u'dt', u'dd', u'img',
)
_htmlsingleonly = ( # Elements that cannot have close tags
	u'br', u'hr', u'img',
)
_htmlnest = ( # Tags that can be nested--??
	u'table', u'tr', u'td', u'th', u'div', u'blockquote', u'ol', u'ul',
	u'dl', u'font', u'big', u'small', u'sub', u'sup', u'span', u'img',
)
_tabletags = ( # Can only appear inside table
	u'td', u'th', u'tr',
)
_htmllist = ( # Tags used by list
	u'ul', u'ol',
)
_listtags = ( # Tags that can appear in a list
	u'li',
)
_htmlsingleallowed = _htmlsingle + _tabletags 
_htmlelements = _htmlsingle + _htmlpairs + _htmlnest

def removeHtmlTags(text):
	"""convert bad tags into HTML identities"""
	sb = []
	text = removeHtmlComments(text)
	bits = text.split(u'<')
	sb.append(bits.pop(0))
	tagstack = []
	tablestack = tagstack
	for x in bits:
		m = _tagPattern.match(x)
		slash, t, params, brace, rest = m.groups()
		t = t.lower()
		badtag = False
		if t in _htmlelements:
			# Check our stack
			if slash:
				# Closing a tag...
				if t in _htmlsingleonly or len(tagstack) == 0:
					badtag = True
				else:
					ot = tagstack.pop()
					if ot != t:
						if ot in _htmlsingleallowed:
							# Pop all elements with an optional close tag
							# and see if we find a match below them
							optstack = []
							optstack.append(ot)
							while True:
								if len(tagstack) == 0:
									break
								ot = tagstack.pop()
								if ot == t or ot not in _htmlsingleallowed:
									break
								optstack.append(ot)
							if t != ot:
								# No match. Push the optinal elements back again
								badtag = True
								tagstack += reversed(optstack)
						else:
							tagstack.append(ot)
							# <li> can be nested in <ul> or <ol>, skip those cases:
							if ot not in _htmllist and t in listtags:
								badtag = True
					elif t == u'table':
						if len(tablestack) == 0:
							bagtag = True
						else:
							tagstack = tablestack.pop()
				newparams = u''
			else:
				# Keep track for later
				if t in _tabletags and u'table' not in tagstack:
					badtag = True
				elif t in tagstack and t not in _htmlnest:
					badtag = True
				# Is it a self-closed htmlpair? (bug 5487)
				elif brace == u'/>' and t in _htmlpairs:
					badTag = True
				elif t in _htmlsingleonly:
					# Hack to force empty tag for uncloseable elements
					brace = u'/>'
				elif t in _htmlsingle:
					# Hack to not close $htmlsingle tags
					brace = None
				else:
					if t == u'table':
						tablestack.append(tagstack)
						tagstack = []
					tagstack.append(t)
				newparams = fixTagAttributes(params, t)
			if not badtag:
				rest = rest.replace(u'>', u'&gt;')
				if brace == u'/>':
					close = u' /'
				else:
					close = u''
				sb.append(u'<')
				sb.append(slash)
				sb.append(t)
				sb.append(newparams)
				sb.append(close)
				sb.append(u'>')
				sb.append(rest)
				continue
		sb.append(u'&lt;')
		sb.append(x.replace(u'>', u'&gt;'))
	
	# Close off any remaining tags
	while tagstack:
		t = tagstack.pop()
		sb.append(u'</')
		sb.append(t)
		sb.append(u'>\n')
		if t == u'table':
			if not tablestack:
				break
			tagstack = tablestack.pop()
	
	return u''.join(sb)

_htmlEntities = {
	u'Aacute':	 193,
	u'aacute':	 225,
	u'Acirc':	  194,
	u'acirc':	  226,
	u'acute':	  180,
	u'AElig':	  198,
	u'aelig':	  230,
	u'Agrave':	 192,
	u'agrave':	 224,
	u'alefsym':	8501,
	u'Alpha':	  913,
	u'alpha':	  945,
	u'amp':		38,
	u'and':		8743,
	u'ang':		8736,
	u'Aring':	  197,
	u'aring':	  229,
	u'asymp':	  8776,
	u'Atilde':	 195,
	u'atilde':	 227,
	u'Auml':	   196,
	u'auml':	   228,
	u'bdquo':	  8222,
	u'Beta':	   914,
	u'beta':	   946,
	u'brvbar':	 166,
	u'bull':	   8226,
	u'cap':		8745,
	u'Ccedil':	 199,
	u'ccedil':	 231,
	u'cedil':	  184,
	u'cent':	   162,
	u'Chi':		935,
	u'chi':		967,
	u'circ':	   710,
	u'clubs':	  9827,
	u'cong':	   8773,
	u'copy':	   169,
	u'crarr':	  8629,
	u'cup':		8746,
	u'curren':	 164,
	u'dagger':	 8224,
	u'Dagger':	 8225,
	u'darr':	   8595,
	u'dArr':	   8659,
	u'deg':		176,
	u'Delta':	  916,
	u'delta':	  948,
	u'diams':	  9830,
	u'divide':	 247,
	u'Eacute':	 201,
	u'eacute':	 233,
	u'Ecirc':	  202,
	u'ecirc':	  234,
	u'Egrave':	 200,
	u'egrave':	 232,
	u'empty':	  8709,
	u'emsp':	   8195,
	u'ensp':	   8194,
	u'Epsilon':	917,
	u'epsilon':	949,
	u'equiv':	  8801,
	u'Eta':		919,
	u'eta':		951,
	u'ETH':		208,
	u'eth':		240,
	u'Euml':	   203,
	u'euml':	   235,
	u'euro':	   8364,
	u'exist':	  8707,
	u'fnof':	   402,
	u'forall':	 8704,
	u'frac12':	 189,
	u'frac14':	 188,
	u'frac34':	 190,
	u'frasl':	  8260,
	u'Gamma':	  915,
	u'gamma':	  947,
	u'ge':		 8805,
	u'gt':		 62,
	u'harr':	   8596,
	u'hArr':	   8660,
	u'hearts':	 9829,
	u'hellip':	 8230,
	u'Iacute':	 205,
	u'iacute':	 237,
	u'Icirc':	  206,
	u'icirc':	  238,
	u'iexcl':	  161,
	u'Igrave':	 204,
	u'igrave':	 236,
	u'image':	  8465,
	u'infin':	  8734,
	u'int':		8747,
	u'Iota':	   921,
	u'iota':	   953,
	u'iquest':	 191,
	u'isin':	   8712,
	u'Iuml':	   207,
	u'iuml':	   239,
	u'Kappa':	  922,
	u'kappa':	  954,
	u'Lambda':	 923,
	u'lambda':	 955,
	u'lang':	   9001,
	u'laquo':	  171,
	u'larr':	   8592,
	u'lArr':	   8656,
	u'lceil':	  8968,
	u'ldquo':	  8220,
	u'le':		 8804,
	u'lfloor':	 8970,
	u'lowast':	 8727,
	u'loz':		9674,
	u'lrm':		8206,
	u'lsaquo':	 8249,
	u'lsquo':	  8216,
	u'lt':		 60,
	u'macr':	   175,
	u'mdash':	  8212,
	u'micro':	  181,
	u'middot':	 183,
	u'minus':	  8722,
	u'Mu':		 924,
	u'mu':		 956,
	u'nabla':	  8711,
	u'nbsp':	   160,
	u'ndash':	  8211,
	u'ne':		 8800,
	u'ni':		 8715,
	u'not':		172,
	u'notin':	  8713,
	u'nsub':	   8836,
	u'Ntilde':	 209,
	u'ntilde':	 241,
	u'Nu':		 925,
	u'nu':		 957,
	u'Oacute':	 211,
	u'oacute':	 243,
	u'Ocirc':	  212,
	u'ocirc':	  244,
	u'OElig':	  338,
	u'oelig':	  339,
	u'Ograve':	 210,
	u'ograve':	 242,
	u'oline':	  8254,
	u'Omega':	  937,
	u'omega':	  969,
	u'Omicron':	927,
	u'omicron':	959,
	u'oplus':	  8853,
	u'or':		 8744,
	u'ordf':	   170,
	u'ordm':	   186,
	u'Oslash':	 216,
	u'oslash':	 248,
	u'Otilde':	 213,
	u'otilde':	 245,
	u'otimes':	 8855,
	u'Ouml':	   214,
	u'ouml':	   246,
	u'para':	   182,
	u'part':	   8706,
	u'permil':	 8240,
	u'perp':	   8869,
	u'Phi':		934,
	u'phi':		966,
	u'Pi':		 928,
	u'pi':		 960,
	u'piv':		982,
	u'plusmn':	 177,
	u'pound':	  163,
	u'prime':	  8242,
	u'Prime':	  8243,
	u'prod':	   8719,
	u'prop':	   8733,
	u'Psi':		936,
	u'psi':		968,
	u'quot':	   34,
	u'radic':	  8730,
	u'rang':	   9002,
	u'raquo':	  187,
	u'rarr':	   8594,
	u'rArr':	   8658,
	u'rceil':	  8969,
	u'rdquo':	  8221,
	u'real':	   8476,
	u'reg':		174,
	u'rfloor':	 8971,
	u'Rho':		929,
	u'rho':		961,
	u'rlm':		8207,
	u'rsaquo':	 8250,
	u'rsquo':	  8217,
	u'sbquo':	  8218,
	u'Scaron':	 352,
	u'scaron':	 353,
	u'sdot':	   8901,
	u'sect':	   167,
	u'shy':		173,
	u'Sigma':	  931,
	u'sigma':	  963,
	u'sigmaf':	 962,
	u'sim':		8764,
	u'spades':	 9824,
	u'sub':		8834,
	u'sube':	   8838,
	u'sum':		8721,
	u'sup':		8835,
	u'sup1':	   185,
	u'sup2':	   178,
	u'sup3':	   179,
	u'supe':	   8839,
	u'szlig':	  223,
	u'Tau':		932,
	u'tau':		964,
	u'there4':	 8756,
	u'Theta':	  920,
	u'theta':	  952,
	u'thetasym':   977,
	u'thinsp':	 8201,
	u'THORN':	  222,
	u'thorn':	  254,
	u'tilde':	  732,
	u'times':	  215,
	u'trade':	  8482,
	u'Uacute':	 218,
	u'uacute':	 250,
	u'uarr':	   8593,
	u'uArr':	   8657,
	u'Ucirc':	  219,
	u'ucirc':	  251,
	u'Ugrave':	 217,
	u'ugrave':	 249,
	u'uml':		168,
	u'upsih':	  978,
	u'Upsilon':	933,
	u'upsilon':	965,
	u'Uuml':	   220,
	u'uuml':	   252,
	u'weierp':	 8472,
	u'Xi':		 926,
	u'xi':		 958,
	u'Yacute':	 221,
	u'yacute':	 253,
	u'yen':		165,
	u'Yuml':	   376,
	u'yuml':	   255,
	u'Zeta':	   918,
	u'zeta':	   950,
	u'zwj':		8205,
	u'zwnj':	   8204
}

_charRefsPat = re.compile(ur'''(&([A-Za-z0-9]+);|&#([0-9]+);|&#[xX]([0-9A-Za-z]+);|(&))''', re.UNICODE)

def validateCodepoint(codepoint):
	return codepoint ==	0x09 \
		or codepoint ==	0x0a \
		or codepoint ==	0x0d \
		or (codepoint >=	0x20 and codepoint <=   0xd7ff) \
		or (codepoint >=  0xe000 and codepoint <=   0xfffd) \
		or (codepoint >= 0x10000 and codepoint <= 0x10ffff)

def _normalizeCallback(match):
	text, norm, dec, hexval, _ = match.groups()
	if norm:
		sb = []
		sb.append(u'&')
		if norm not in _htmlEntities:
			sb.append(u'amp;')
		sb.append(norm)
		sb.append(u';')
		return u''.join(sb)
	elif dec:
		dec = int(dec)
		if validateCodepoint(dec):
			sb = []
			sb.append(u'&#')
			sb.append(dec)
			sb.append(u';')
			return u''.join(sb)
	elif hexval:
		hexval = int(hexval, 16)
		if validateCodepoint(hexval):
			sb = []
			sb.append(u'&#x')
			sb.append(hex(hexval))
			sb.append(u';')
			return u''.join(sb)
	return text.replace(u'&', u'&amp;').replace(u'<', u'&lt;').replace(u'>', u'&gt;')

def normalizeCharReferences(text):
	"""docstring for normalizeCharReferences"""
	return _charRefsPat.sub(_normalizeCallback, text)

def _decodeCallback(match):
	text, norm, dec, hexval, _ = match.groups()
	if norm:
		if norm in _htmlEntities:
			return unichr(_htmlEntities[norm])
		else:
			sb = []
			sb.append(u'&')
			sb.append(norm)
			sb.append(u';')
			return u''.join(sb)
	elif dec:
		dec = int(dec)
		if validateCodepoint(dec):
			return unichr(dec)
		return u'?'
	elif hexval:
		hexval = int(hexval, 16)
		if validateCodepoint(dec):
			return unichr(dec)
		return u'?'
	return text

def decodeCharReferences(text):
	"""docstring for decodeCharReferences"""
	if text:
		return _charRefsPat.sub(_decodeCallback, text)
	return ''

_cssCommentPat = re.compile(ur'''\*.*?\*''', re.UNICODE)
_toUTFPat = re.compile(ur'''\\([0-9A-Fa-f]{1,6})[\s]?''', re.UNICODE)
_hackPat = re.compile(ur'''(expression|tps*://|url\s*\().*''', re.UNICODE | re.IGNORECASE)

def _convertToUtf8(s):
	return unichr(int(s.group(1), 16))

def checkCss(value):
	"""docstring for checkCss"""
	stripped = decodeCharReferences(value)
	
	stripped = _cssCommentPat.sub(u'', stripped)
	value = stripped
	
	stripped = _toUTFPat.sub(_convertToUtf8, stripped)
	stripped.replace(u'\\', u'')
	if _hackPat.search(stripped):
		# someone is haxx0ring
		return False
	
	return value

def escapeId(value):
	"""docstring for escapeId"""
	# TODO
	return slugifyBit(value)

_hrPat = re.compile(u'''^-----*''', re.UNICODE | re.MULTILINE)
def parseHorizontalRule(text):
	return _hrPat.sub(ur'<hr />', text)

_h1Pat = re.compile(u'''^=(.+)=\s*$''', re.UNICODE | re.MULTILINE)
_h2Pat = re.compile(u'''^==(.+)==\s*$''', re.UNICODE | re.MULTILINE)
_h3Pat = re.compile(u'''^===(.+)===\s*$''', re.UNICODE | re.MULTILINE)
_h4Pat = re.compile(u'''^====(.+)====\s*$''', re.UNICODE | re.MULTILINE)
_h5Pat = re.compile(u'''^=====(.+)=====\s*$''', re.UNICODE | re.MULTILINE)
_h6Pat = re.compile(u'''^======(.+)======\s*$''', re.UNICODE | re.MULTILINE)
def parseHeaders(text):
	text = _h6Pat.sub(ur'<h6>\1</h6>', text)
	text = _h5Pat.sub(ur'<h5>\1</h5>', text)
	text = _h4Pat.sub(ur'<h4>\1</h4>', text)
	text = _h3Pat.sub(ur'<h3>\1</h3>', text)
	text = _h2Pat.sub(ur'<h2>\1</h2>', text)
	text = _h1Pat.sub(ur'<h1>\1</h1>', text)
	return text

_quotePat = re.compile(u"""(''+)""", re.UNICODE)
def parseQuotes(text):
	arr = _quotePat.split(text)
	if len(arr) == 1:
		return text
	# First, do some preliminary work. This may shift some apostrophes from
	# being mark-up to being text. It also counts the number of occurrences
	# of bold and italics mark-ups.
	numBold = 0
	numItalics = 0
	for i,r in zip(range(len(arr)), arr):
		if i%2 == 1:
			l = len(r)
			if l == 4:
				arr[i-1] += u"'"
				arr[i] = u"'''"
			elif l > 5:
				arr[i-1] += u"'" * (len(arr[i]) - 5)
				arr[i] = u"'''''"
			if l == 2:
				numItalics += 1
			elif l >= 5:
				numItalics += 1
				numBold += 1
			else:
				numBold += 1
	
	# If there is an odd number of both bold and italics, it is likely
	# that one of the bold ones was meant to be an apostrophe followed
	# by italics. Which one we cannot know for certain, but it is more
	# likely to be one that has a single-letter word before it.
	if numBold%2 == 1 and numItalics%2 == 1:
		firstSingleLetterWord = -1
		firstMultiLetterWord = -1
		firstSpace = -1
		for i,r in zip(range(len(arr)), arr):
			if i%2 == 1 and len(r) == 3:
				x1 = arr[i-1][-1:]
				x2 = arr[i-1][-2:-1]
				if x1 == u' ':
					if firstSpace == -1:
						firstSpace = i
				elif x2 == u' ':
					if firstSingleLetterWord == -1:
						firstSingleLetterWord = i
				else:
					if firstMultiLetterWord == -1:
						firstMultiLetterWord = i
		
		# If there is a single-letter word, use it!
		if firstSingleLetterWord > -1:
			arr[firstSingleLetterWord] = u"''"
			arr[firstSingleLetterWord-1] += u"'"
		# If not, but there's a multi-letter word, use that one.
		elif firstMultiLetterWord > -1:
			arr[firstMultiLetterWord] = u"''"
			arr[firstMultiLetterWord-1] += u"'"
		# ... otherwise use the first one that has neither.
		# (notice that it is possible for all three to be -1 if, for example,
		# there is only one pentuple-apostrophe in the line)
		elif firstSpace > -1:
			arr[firstSpace] = u"''"
			arr[firstSpace-1] += u"'"
	
	# Now let's actually convert our apostrophic mush to HTML!
	output = []
	buffer = None
	state = ''
	for i,r in zip(range(len(arr)), arr):
		if i%2 == 0:
			if state == 'both':
				buffer.append(r)
			else:
				output.append(r)
		else:
			if len(r) == 2:
				if state == 'i':
					output.append(u"</i>")
					state = ''
				elif state == 'bi':
					output.append(u"</i>")
					state = 'b'
				elif state == 'ib':
					output.append(u"</b></i><b>")
					state = 'b'
				elif state == 'both':
					output.append(u"<b><i>")
					output.append(u''.join(buffer))
					buffer = None
					output.append(u"</i>")
					state = 'b'
				elif state == 'b':
					output.append(u"<i>")
					state = 'bi'
				else: # ''
					output.append(u"<i>")
					state = 'i'
			elif len(r) == 3:
				if state == 'b':
					output.append(u"</b>")
					state = ''
				elif state == 'bi':
					output.append(u"</i></b><i>")
					state = 'i'
				elif state == 'ib':
					output.append(u"</b>")
					state = 'i'
				elif state == 'both':
					output.append(u"<i><b>")
					output.append(u''.join(buffer))
					buffer = None
					output.append(u"</b>")
					state = 'i'
				elif state == 'i':
					output.append(u"<b>")
					state = 'ib'
				else: # ''
					output.append(u"<b>")
					state = 'b'
			elif len(r) == 5:
				if state == 'b':
					output.append(u"</b><i>")
					state = 'i'
				elif state == 'i':
					output.append(u"</i><b>")
					state = 'b'
				elif state == 'bi':
					output.append(u"</i></b>")
					state = ''
				elif state == 'ib':
					output.append(u"</b></i>")
					state = ''
				elif state == 'both':
					output.append(u"<i><b>")
					output.append(u''.join(buffer))
					buffer = None
					output.append(u"</b></i>")
					state = ''
				else: # ''
					buffer = []
					state = 'both'
	
	if state == 'both':
		output.append(u"<i><b>")
		output.append(u''.join(buffer))
		buffer = None
		output.append(u"</b></i>")
	elif state != '':
		if state == 'b' or state == 'ib':
			output.append(u"</b>")
		if state == 'i' or state == 'bi' or state == 'ib':
			output.append(u"</i>")
		if state == 'bi':
			output.append(u"</b>")
	return u''.join(output)

def parseAllQuotes(text):
	sb = []
	lines = text.split(u'\n')
	first = True
	for line in lines:
		if not first:
			sb.append(u'\n')
		else:
			first = False
		sb.append(parseQuotes(line))
	return u''.join(sb)

_removePat = re.compile(ur'\b(' + ur'|'.join((u"a", u"an", u"as", u"at", u"before", u"but", u"by", u"for", u"from",
							u"is", u"in", u"into", u"like", u"of", u"off", u"on", u"onto", u"per",
							u"since", u"than", u"the", u"this", u"that", u"to", u"up", u"via",
							u"with")) + ur')\b', re.UNICODE | re.IGNORECASE)
_nonWordSpaceDashPat = re.compile(ur'[^\w\s\-\./]', re.UNICODE)
_multiSpacePat = re.compile(ur'[\s\-_\./]+', re.UNICODE)
_spacePat = re.compile(ur' ', re.UNICODE)

def slugifyBit(bit):
	#bit = _removePat.sub(u'', bit)
	bit = _nonWordSpaceDashPat.sub(u'', bit)
	bit = _multiSpacePat.sub(u' ', bit)
	bit = bit.strip()
	bit = _spacePat.sub(u'-', bit)
	bit = bit.lower()
	return bit

def slugify(text):
	"""docstring for slugify"""
	return u'/'.join(slugifyBit(t) for t in text.split(u'/'))

_linkPat = re.compile(ur'^([A-Za-z0-9\s]+:)?([A-Za-z0-9_\.\-\s\/]+)(?:\|([^\n]+?))?\]\](.*)$', re.UNICODE | re.DOTALL)
def replaceInternalLinks(text):
	arr = text.split('[[')
	sb = []
	sb.append(arr.pop(0))
	for bit in arr:
		namespace, link, alt, rest = None, None, None, None
		match = _linkPat.match(bit)
		if match:
			namespace, link, alt, rest = match.groups()
		if link:
			if not namespace:
				namespace = u'wiki'
			namespace = slugify(namespace)
			if namespace == "image":
				sb.append(u'<a href="/image/')
				sb.append(slugify(link))
				sb.append(u'"><img src="/static/')
				sb.append(link)
				if alt:
					sb.append(u'" alt="')
					sb.append(alt)
				sb.append(u'" /></a>')
			elif namespace == 'wiki':
				sb.append(u'<a href="/')
				sb.append(namespace)
				sb.append(u'/')
				sb.append(slugify(link))
				if alt:
					link = alt
				sb.append(u'/">')
				sb.append(link)
				sb.append(u'</a>')
			sb.append(rest)
		else:
			sb.append(u'[[')
			sb.append(bit)
	return u''.join(sb)


def checkTOC(text):
	showToc = True
	if text.find(u"__NOTOC__") != -1:
		text = text.replace(u"__NOTOC__", u"")
		showToc = False
	if text.find(u"__TOC__") != -1:
		text = text.replace(u"__TOC__", u"<!--MWTOC-->")
		showToc = True
	return text, showToc

_bracketedLinkPat = re.compile(ur'(?:\[((?:https?://|ftp://|/)[^<>\]\[' + u"\x00-\x20\x7f" + ur']+)\s*(.*?)\])', re.UNICODE)
def replaceExternalLinks(text):
	sb = []
	bits = _bracketedLinkPat.split(text)
	l = len(bits)
	i = 0
	num_links = 0
	while i < l:
		if i%3 == 0:
			sb.append(replaceFreeExternalLinks(bits[i]))
			i += 1
		else:
			sb.append(u'<a href="')
			sb.append(bits[i])
			sb.append(u'">')
			if not bits[i+1]:
				sb.append(u'[')
				num_links += 1
				sb.append(to_unicode(num_links))
				sb.append(u']')
			else:
				sb.append(bits[i+1])
			sb.append(u'</a>')
			i += 2
	return ''.join(sb)

_protocolPat = re.compile(ur'(\b(?:https?://|ftp://))', re.UNICODE)
_specialUrlPat = re.compile(ur'^([^<>\]\[' + u"\x00-\x20\x7f" + ur']+)(.*)$', re.UNICODE)
_protocolsPat = re.compile(ur'^(https?://|ftp://)$', re.UNICODE)

def replaceFreeExternalLinks(text):
	bits = _protocolPat.split(text)
	sb = [bits.pop(0)]
	i = 0
	l = len(bits)
	while i < l:
		protocol = bits[i]
		remainder = bits[i+1]
		i += 2
		match = _specialUrlPat.match(remainder)
		if match:
			# Found some characters after the protocol that look promising
			url = protocol + match.group(1)
			trail = match.group(2)
			
			# special case: handle urls as url args:
			# http://www.example.com/foo?=http://www.example.com/bar
			if len(trail) == 0 and len(bits) > i and _protocolsPat.match(bits[i]):
				match = _specialUrlPat.match(remainder)
				if match:
					url += bits[i] + match.groups(1)
					i += 2
					trail = m[2]
			
			# The characters '<' and '>' (which were escaped by
			# removeHTMLtags()) should not be included in
			# URLs, per RFC 2396.
			pos = max(url.find('&lt;'), url.find('&gt;'))
			if pos != -1:
				trail = url[pos:] + trail
				url = url[0:pos]
			
			sep = ',;.:!?'
			if '(' not in url:
				sep += ')'
				
			i = len(url)-1
			while i >= 0:
				char = url[i]
				if char not in sep:
					break
				i -= 1
			i += 1
			
			if i != len(url):
				trail = url[i:] + trail
				url = url[0:i]
			
			url = cleanURL(url)
			
			sb.append(u'<a href="')
			sb.append(url)
			sb.append(u'">')
			sb.append(url)
			sb.append(u'</a>')
			sb.append(text)
			sb.append(trail)
		else:
			sb.append(protocol)
			sb.append(remainder)
	return ''.join(sb)

def urlencode(char):
	num = ord(char)
	if num == 32:
		return '+'
	return "%%%02x" % num

_controlCharsPat = re.compile(ur'[\]\[<>"' + u"\\x00-\\x20\\x7F" + ur']]', re.UNICODE)
_hostnamePat = re.compile(ur'^([^:]+:)(//[^/]+)?(.*)$', re.UNICODE)
_stripPat = re.compile(u'\\s|\u00ad|\u1806|\u200b|\u2060|\ufeff|\u03f4|\u034f|\u180b|\u180c|\u180d|\u200c|\u200d|[\ufe00-\ufe0f]', re.UNICODE)
def cleanURL(url):
	# Normalize any HTML entities in input. They will be
	# re-escaped by makeExternalLink().
	url = decodeCharReferences(url)
	
	# Escape any control characters introduced by the above step
	url = _controlCharsPat.sub(urlencode, url)
	
	# Validate hostname portion
	match = _hostnamePat.match(url)
	if match:
		protocol, host, rest = match.groups()
		
		# Characters that will be ignored in IDNs.
		# http://tools.ietf.org/html/3454#section-3.1
		# Strip them before further processing so blacklists and such work.
		
		_stripPat.sub('', host)
		
		# @fixme: validate hostnames here
		
		return protocol + host + rest
	else:
		return url

_zomgPat = re.compile(ur'^(:*)\{\|(.*)$', re.UNICODE)

def doTableStuff(text, state):
	t = text.split(u"\n")
	td = [] # Is currently a td tag open?
	ltd = [] # Was it TD or TH?
	tr = [] # Is currently a tr tag open?
	ltr = [] # tr attributes
	has_opened_tr = [] # Did this table open a <tr> element?
	indent_level = 0 # indent level of the table
	
	for k, x in zip(range(len(t)), t):
		x = x.strip()
		fc = x[0:1]
		matches = _zomgPat.match(x)
		if matches:
			indent_level = len(matches.group(1))
			
			attributes = unstripForHTML(matches.group(2), state)
			
			t[k] = u'<dl><dd>'*indent_level + u'<table' + fixTagAttributes(attributes, u'table') + u'>'
			td.append(False)
			ltd.append(u'')
			tr.append(False)
			ltr.append(u'')
			has_opened_tr.append(False)
		elif len(td) == 0:
			pass
		elif u'|}' == x[0:2]:
			z = u"</table>" + x[2:]
			l = ltd.pop()
			if not has_opened_tr.pop():
				z = u"<tr><td></td><tr>" + z
			if tr.pop():
				z = u"</tr>" + z
			if td.pop():
				z = u'</' + l + u'>' + z
			ltr.pop()
			t[k] = z + u'</dd></dl>'*indent_level
		elif u'|-' == x[0:2]: # Allows for |-------------
			x = x[1:]
			while x != u'' and x[0:1] == '-':
				x = x[1:]
			z = ''
			l = ltd.pop()
			has_opened_tr.pop()
			has_opened_tr.append(True)
			if tr.pop():
				z = u'</tr>' + z
			if td.pop():
				z = u'</' + l + u'>' + z
			ltr.pop()
			t[k] = z
			tr.append(False)
			td.append(False)
			ltd.append(u'')
			attributes = unstripForHTML(x, state)
			ltr.append(fixTagAttributes(attributes, u'tr'))
		elif u'|' == fc or u'!' == fc or u'|+' == x[0:2]: # Caption
			# x is a table row
			if u'|+' == x[0:2]:
				fc = u'+'
				x = x[1:]
			x = x[1:]
			if fc == u'!':
				x = x.replace(u'!!', u'||')
			# Split up multiple cells on the same line.
			# FIXME: This can result in improper nesting of tags processed
			# by earlier parser steps, but should avoid splitting up eg
			# attribute values containing literal "||".
			x = x.split(u'||')
			
			t[k] = u''
			
			# Loop through each table cell
			for theline in x:
				z = ''
				if fc != u'+':
					tra = ltr.pop()
					if not tr.pop():
						z = u'<tr' + tra + u'>\n'
					tr.append(True)
					ltr.append(u'')
					has_opened_tr.pop()
					has_opened_tr.append(True)
				l = ltd.pop()
				if td.pop():
					z = u'</' + l + u'>' + z
				if fc == u'|':
					l = u'td'
				elif fc == u'!':
					l = u'th'
				elif fc == u'+':
					l = u'caption'
				else:
					l = u''
				ltd.append(l)
				
				#Cell parameters
				y = theline.split(u'|', 1)
				# Note that a '|' inside an invalid link should not
				# be mistaken as delimiting cell parameters
				if y[0].find(u'[[') != -1:
					y = [theline]
					
				if len(y) == 1:
					y = z + u"<" + l + u">" + y[0]
				else:
					attributes = unstripForHTML(y[0], state)
					y = z + u"<" + l + fixTagAttributes(attributes, l) + u">" + y[1]
				
				t[k] += y
				td.append(True)
	
	while len(td) > 0:
		l = ltd.pop()
		if td.pop():
			t.append(u'</td>')
		if tr.pop():
			t.append(u'</tr>')
		if not has_opened_tr.pop():
			t.append(u'<tr><td></td></tr>')
		t.append(u'</table>')
	
	text = u'\n'.join(t)
	# special case: don't return empty table
	if text == u"<table>\n<tr><td></td></tr>\n</table>":
		text = u''
	
	return text

def unstripForHTML(text, state):
	text = unstrip(text, state)
	text = unstripNoWiki(text, state)
	return text

def unstrip(text, state):
	if 'general' not in state:
		return text

	general = state['general']
	for k in general:
		v = general[k]
		text = text.replace(k, v)
	return text

def unstripNoWiki(text, state):
	if 'nowiki' not in state:
		return text
	nowiki = state['nowiki']
	for k in nowiki:
		v = nowiki[k]
		text = text.replace(k, v)
	return text

_headerPat = re.compile(ur"<[Hh]([1-6])(.*?)>(.*?)</[Hh][1-6] *>", re.UNICODE)
_templateSectionPat = re.compile(ur"<!--MWTEMPLATESECTION=([^&]+)&([^_]+)-->", re.UNICODE)
_tagPat = re.compile(ur"<.*?>", re.UNICODE)
def formatHeadings(text, isMain, showToc, state):
	"""
	This function accomplishes several tasks:
	1) Auto-number headings if that option is enabled
	2) Add an [edit] link to sections for logged in users who have enabled the option
	3) Add a Table of contents on the top for users who have enabled the option
	4) Auto-anchor headings
	
	It loops through all headlines, collects the necessary data, then splits up the
	string and re-inserts the newly formatted headlines.
	"""
	doNumberHeadings = False
	showEditLink = True # Can User Edit

	if text.find(u"__NOEDITSECTION__") != -1:
		showEditLink = False
		text = text.replace(u"__NOEDITSECTION__", u"")

	# Get all headlines for numbering them and adding funky stuff like [edit]
	# links - this is for later, but we need the number of headlines right now
	matches = _headerPat.findall(text)
	numMatches = len(matches)

	# if there are fewer than 4 headlines in the article, do not show TOC
	# unless it's been explicitly enabled.
	enoughToc = showToc and (numMatches >= 4 or text.find(u"<!--MWTOC-->") != -1)
	
	# Allow user to stipulate that a page should have a "new section"
	# link added via __NEWSECTIONLINK__
	showNewSection = False
	if text.find(u"__NEWSECTIONLINK__") != -1:
		showNewSection = True
		text = text.replace(u"__NEWSECTIONLINK__", u"")
	# if the string __FORCETOC__ (not case-sensitive) occurs in the HTML,
	# override above conditions and always show TOC above first header
	if text.find(u"__FORCETOC__") != -1:
		showToc = True
		enoughToc = True
		text = text.replace(u"__FORCETOC__", u"")
	# Never ever show TOC if no headers
	if numMatches < 1:
		enoughToc = False

	# headline counter
	headlineCount = 0
	sectionCount = 0 # headlineCount excluding template sections

	# Ugh .. the TOC should have neat indentation levels which can be
	# passed to the skin functions. These are determined here
	toc = []
	head = {}
	sublevelCount = {}
	levelCount = {}
	toclevel = 0
	level = 0
	prevlevel = 0
	toclevel = 0
	prevtoclevel = 0
	refers = {}
	refcount = {}
	wgMaxTocLevel = 5
	
	for match in matches:
		headline = match[2]
		istemplate = False
		templatetitle = u''
		templatesection = 0
		numbering = []
		
		m = _templateSectionPat.search(headline)
		if m:
			istemplate = True
			templatetitle = b64decode(m[0])
			templatesection = 1 + int(b64decode(m[1]))
			headline = _templateSectionPat.sub(u'', headline)
		
		if toclevel:
			prevlevel = level
			prevtoclevel = toclevel
		
		level = matches[headlineCount][0]
		
		if doNumberHeadings or enoughToc:
			if level > prevlevel:
				toclevel += 1
				sublevelCount[toclevel] = 0
				if toclevel < wgMaxTocLevel:
					toc.append(u'\n<ul>')
			elif level < prevlevel and toclevel > 1:
				# Decrease TOC level, find level to jump to
				
				if toclevel == 2 and level < levelCount[1]:
					toclevel = 1
				else:
					for i in range(toclevel, 0, -1):
						if levelCount[i] == level:
							# Found last matching level
							toclevel = i
							break
						elif levelCount[i] < level:
							toclevel = i + 1
							break
				if toclevel < wgMaxTocLevel:
					toc.append(u"</li>\n")
					toc.append(u"</ul>\n</li>\n" * max(prevtoclevel - toclevel, 0))
			else:
				if toclevel < wgMaxTocLevel:
					toc.append(u"</li>\n")
			
			levelCount[toclevel] = level
			
			# count number of headlines for each level
			sublevelCount[toclevel] += 1
			for i in range(1, toclevel+1):
				if sublevelCount[i]:
					numbering.append(to_unicode(sublevelCount[i]))
		
		# The canonized header is a version of the header text safe to use for links
		# Avoid insertion of weird stuff like <math> by expanding the relevant sections
		canonized_headline = unstrip(headline, state)
		canonized_headline = unstripNoWiki(canonized_headline, state)
		
		# -- don't know what to do with this yet.
		# Remove link placeholders by the link text.
		#	 <!--LINK number-->
		# turns into
		#	 link text with suffix
#		$canonized_headline = preg_replace( '/<!--LINK ([0-9]*)-->/e',
#							"\$this->mLinkHolders['texts'][\$1]",
#							$canonized_headline );
#		$canonized_headline = preg_replace( '/<!--IWLINK ([0-9]*)-->/e',
#							"\$this->mInterwikiLinkHolders['texts'][\$1]",
#							$canonized_headline );

		# strip out HTML
		canonized_headline = _tagPat.sub(u'', canonized_headline)
		tocline = canonized_headline.strip()
		# Save headline for section edit hint before it's escaped
		headline_hint = tocline
		canonized_headline = escapeId(tocline)
		refers[headlineCount] = canonized_headline

		# count how many in assoc. array so we can track dupes in anchors
		if canonized_headline not in refers:
			refers[canonized_headline] = 1
		else:
			refers[canonized_headline] += 1
		refcount[headlineCount] = refers[canonized_headline]
		
		numbering = '.'.join(numbering)
		
		# Don't number the heading if it is the only one (looks silly)
		if doNumberHeadings and numMatches > 1:
			# the two are different if the line contains a link
			headline = numbering + u' ' + headline

		# Create the anchor for linking from the TOC to the section
		anchor = canonized_headline;
		if refcount[headlineCount] > 1:
			anchor += u'_' + unicode(refcount[headlineCount])
		
		if enoughToc:
			toc.append(u'\n<li class="toclevel-')
			toc.append(to_unicode(toclevel))
			toc.append(u'"><a href="#')
			toc.append(anchor)
			toc.append(u'"><span class="tocnumber">')
			toc.append(numbering)
			toc.append(u'</span> <span class="toctext">')
			toc.append(tocline)
			toc.append(u'</span></a>')
		
#		if showEditLink and (not istemplate or templatetitle != u""):
#			if not head[headlineCount]:
#				head[headlineCount] = u''
#			
#			if istemplate:
#				head[headlineCount] += sk.editSectionLinkForOther(templatetile, templatesection)
#			else:
#				head[headlineCount] += sk.editSectionLink(mTitle, sectionCount+1, headline_hint)
		
		# give headline the correct <h#> tag
		if headlineCount not in head:
			head[headlineCount] = []
		h = head[headlineCount]
		h.append(u'<h')
		h.append(to_unicode(level))
		h.append(u' id="')
		h.append(anchor)
		h.append('">')
		h.append(matches[headlineCount][1].strip())
		h.append(headline.strip())
		h.append(u'</h')
		h.append(to_unicode(level))
		h.append(u'>')
		
		headlineCount += 1

		if not istemplate:
			sectionCount += 1
		
	if enoughToc:
		if toclevel < wgMaxTocLevel:
			toc.append(u"</li>\n")
			toc.append(u"</ul>\n</li>\n" * max(0, toclevel - 1))
		toc.insert(0, u'<table id="toc" class="toc" summary="Contents"><tr><td><div id="toctitle"><h2>Contents</h2></div>')
		toc.append(u'</ul>\n</td></tr></table>')

	# split up and insert constructed headlines
	
	blocks = _headerPat.split(text)
	
	i = 0
	len_blocks = len(blocks)
	forceTocPosition = text.find(u"<!--MWTOC-->")
	full = []
	while i < len_blocks:
		j = i/4
		full.append(blocks[i])
		if enoughToc and not i and isMain and forceTocPosition == -1:
			full += toc
			toc = None
		if j in head and head[j]:
			full += head[j]
			head[j] = None
		i += 4
	full = u''.join(full)
	if forceTocPosition != -1:
		return full.replace(u"<!--MWTOC-->", u''.join(toc), 1)
	else:
		return full

_startRegexHash = {}
_endRegexHash = {}
_endCommentPat = re.compile(ur'(-->)', re.UNICODE)
_extractTagsAndParams_n = 1
def extractTagsAndParams(elements, text, matches, uniq_prefix = u''):
	"""
	Replaces all occurrences of HTML-style comments and the given tags
	in the text with a random marker and returns teh next text. The output
	parameter $matches will be an associative array filled with data in
	the form:
	  'UNIQ-xxxxx' => array(
	  'element',
	  'tag content',
	  array( 'param' => 'x' ),
	  '<element param="x">tag content</element>' ) )
	"""
	stripped = u''
	
	taglist = u'|'.join(elements)
	if taglist not in _startRegexHash:
		_startRegexHash[taglist] = re.compile(ur"<(" + taglist + ur")(\s+[^>]*?|\s*?)(/?>)|<(!--)", re.UNICODE | re.IGNORECASE)
	start = _startRegexHash[taglist]
	
	while text != u'':
		p = start.split(text, 1)
		stripped += p[0]
		if len(p) == 1:
			break
		elif p[4]:
			# comment
			element = p[4]
			attributes = u''
			close = u''
		else:
			element = p[1]
			attributes = p[2]
			close = p[3]
		inside = p[5]
		
		global _extractTagsAndParams_n
		marker = uniq_prefix + u'-' + element + u'-' + (u"%08X" % _extractTagsAndParams_n) + u'-QINU'
		_extractTagsAndParams_n += 1
		stripped += marker
		
		if close == u'/>':
			# empty element tag, <tag />
			content = None
			text = inside
			tail = None
		else:
			if element == u'!--':
				end = _endCommentPat
			else:
				if element not in _endRegexHash:
					_endRegexHash[element] = re.compile(ur'(</' + element + ur'\s*>)', re.UNICODE | re.IGNORECASE)
				end = _endRegexHash[element]
			q = end.split(inside, 1)
			content = q[0]
			if len(q) < 3:
				# no end tag
				tail = ''
				text = ''
			else:
				tail = q[1]
				text = q[2]
		
		matches[marker] = (
			element,
			content,
			decodeTagAttributes(attributes),
			u"<" + element + attributes + close + content + tail
		)
	return stripped

def strip(text, state, uniq_prefix, stripcomments = False, dontstrip = []):
	render = True

	commentState = {}
	
	elements = ['nowiki', 'gallery']  + mTagHooks.keys()
	if True: #wgRawHtml
		elements.append('html')
#	if( $this->mOptions->getUseTeX() ) {
#		$elements[] = 'math';
#	}
	
	# Removing $dontstrip tags from $elements list (currently only 'gallery', fixing bug 2700)
	for k in dontstrip:
		if k in elements:
			del elements[k]
	
	matches = {}
	text = extractTagsAndParams(elements, text, matches, uniq_prefix)
	
	for marker in matches:
		element, content, params, tag = matches[marker]
		if render:
			tagName = element.lower()
			if tagName == u'!--':
				# comment
				output = tag
				if tag[-3:] != u'-->':
					output += "-->"
			elif tagName == u'html':
				output = content
			elif tagName == u'nowiki':
				output = content.replace(u'&', u'&amp;').replace(u'<', u'&lt;').replace(u'>', u'&gt;')
			elif tagName == u'math':
				output = content
				# do math here
			elif tagName == u'gallery':
				output = renderImageGallery(content, params)
			else:
				if tagName in mTagHooks:
					output = mTagHooks[tagName](content, params)
				else:
					output = content.replace(u'&', u'&amp;').replace(u'<', u'&lt;').replace(u'>', u'&gt;')
		else:
			# Just stripping tags; keep the source
			output = tag

		# Unstrip the output, because unstrip() is no longer recursive so 
		# it won't do it itself
		output = unstrip(output, state)
		
		if not stripcomments and element == u'!--':
			commentState[marker] = output
		elif element == u'html' or element == u'nowiki':
			if 'nowiki' not in state:
				state['nowiki'] = {}
			state['nowiki'][marker] = output
		else:
			if 'general' not in state:
				state['general'] = {}
			state['general'][marker] = output

	# Unstrip comments unless explicitly told otherwise.
	# (The comments are always stripped prior to this point, so as to
	# not invoke any extension tags / parser hooks contained within
	# a comment.)
	if not stripcomments:
		# Put them all back and forget them
		for k in commentState:
			v = commentState[k]
			text = text.replace(k, v)
	
	return text

mArgStack = []

def replaceVariables(text, args = {}, argsOnly = False):
	"""
	Replace magic variables, templates, and template arguments
	with the appropriate text. Templates are substituted recursively,
	taking care to avoid infinite loops.
	"""
	return text
	# Prevent too big inclusions
#	if( strlen( $text ) > $this->mOptions->getMaxIncludeSize() ) {
#		return $text;
#	}

	# This function is called recursively. To keep track of arguments we need a stack:
	mArgStack.append(args)
	
	braceCallbacks = {}
	if not argsOnly:
		braceCallbacks[2] = [None, braceSubstitution]
	braceCallbacks[3] = [None, argSubstitution]
	
	callbacks = {
		u'{': {
			'end': u'}',
			'cb': braceCallbacks,
			'min': argsOnly and 3 or 2,
			'max': 3
		},
		u'[': {
			'end': u']',
			'cb': {2: None},
			'min': 2,
			'max': 2
		}
	}
	text = replace_callback(text, callbacks)
	mArgStack.pop()
	
	return text

def replace_callback(text, callbacks):
	"""
	parse any parentheses in format ((title|part|part))
	and call callbacks to get a replacement text for any found piece
	"""
	openingBraceStack = []	  # this array will hold a stack of parentheses which are not closed yet
	lastOpeningBrace = -1	   # last not closed parentheses

	validOpeningBraces = u''.join(callbacks.keys())
	
	i = 0
	while i < len(text):
		if lastOpeningBrace == -1:
			currentClosing = u''
			search = validOpeningBraces
		else:
			currentClosing = openingBraceStack[lastOpeningBrace]['braceEnd']
			search = validOpeningBraces + u'|' + currentClosing
		rule = None
		pos = -1
		for c in search:
			pos = max(pos, text.find(c, i))
		pos -= i
		pos += 1
		if pos == 0:
			pos = len(text)-i
		i += pos
		if i < len(text):
			if text[i] == u'|':
				found = 'pipe'
			elif text[i] == currentClosing:
				found = 'close'
			elif text[i] in callbacks:
				found = 'open'
				rule = callbacks[text[i]]
			else:
				i += 1
				continue
		else:
			break
		
		if found == 'open':
			# found opening brace, let's add it to parentheses stack
			piece = {
				'brace': text[i],
				'braceEnd': rule['end'],
				'title': u'',
				'parts': None
			}

			# count opening brace characters
			count = 0
			while True:
				if text[i+count:i+1+count] == piece['brace']:
					count += 1
				else:
					break
			piece['count'] = count
			i += piece['count']
			piece['startAt'] = piece['partStart'] = i

			# we need to add to stack only if opening brace count is enough for one of the rules
			if piece['count'] >= rule['min']:
				lastOpeningBrace += 1
				openingBraceStack[lastOpeningBrace] = piece
		elif found == 'close':
			maxCount = openingBraceStack[lastOpeningBrace]['count']
			count = 0
			while count < maxCount:
				if text[i+count:i+1+count] == text[i]:
					count += 1
				else:
					break
			
			# check for maximum matching characters (if there are 5 closing 
			# characters, we will probably need only 3 - depending on the rules)
			matchingCount = 0
			matchingCallback = None
			cbType = callbacks[openingBraceStack[lastOpeningBrace]['brace']]
			if count > cbType['max']:
				# The specified maximum exists in the callback array, unless the caller 
				# has made an error
				matchingCount = cbType['max']
			else:
				# Count is less than the maximum
				# Skip any gaps in the callback array to find the true largest match
				# Need to use array_key_exists not isset because the callback can be null
				matchingCount = count
				while matchingCount > 0 and matchingCount not in cbType['cb']:
					matchingCount -= 1
			
			if matchingCount <= 0:
				i += count
				continue
			matchingCallback = cbType['cb'][matchingCount]
			
			# let's set a title or last part (if '|' was found)
			if openingBraceStack[lastOpeningBrace]['parts'] is None:
				openingBraceStack[lastOpeningBrace]['title'] = \
					text[openingBraceStack[lastOpeningBrace]['partStart']:i]
			else:
				openingBraceStack[lastOpeningBrace]['parts'].append( 
					text[openingBraceStack[lastOpeningBrace]['partStart']:i]
				)

			pieceStart = openingBraceStack[lastOpeningBrace]['startAt'] - matchingCount
			pieceEnd = i + matchingCount
			
			if callable(matchingCallback):
				cbArgs = {
					'text': text[pieceStart:pieceEnd],
					'title': openingBraceStack[lastOpeningBrace]['title'].strip(),
					'parts': openingBraceStack[lastOpeningBrace]['parts'],
					'lineStart': pieceStart > 0 and text[pieceStart-1] == u"\n"
				}
				# finally we can call a user callback and replace piece of text
				replaceWith = matchingCallback(cbArgs)
				text = text[:pieceStart] + replaceWith + text[pieceEnd:]
				i = pieceStart + len(replaceWith)
			else:
				# null value for callback means that parentheses should be parsed, but not replaced
				i += matchingCount
			
			# reset last opening parentheses, but keep it in case there are unused characters
			piece = {
				'brace': openingBraceStack[lastOpeningBrace]['brace'],   
				'braceEnd': openingBraceStack[lastOpeningBrace]['braceEnd'],
				'count': openingBraceStack[lastOpeningBrace]['count'],
				'title': u'',
				'parts': None,
				'startAt': openingBraceStack[lastOpeningBrace]['startAt']
			}
			openingBraceStack[lastOpeningBrace] = None
			lastOpeningBrace -= 1
			
			if matchingCount < piece['count']:
				piece['count'] -= matchingCount
				piece['startAt'] -= matchingCount
				piece['partStart'] = piece['startAt']
				# do we still qualify for any callback with remaining count?
				currentCbList = callbacks[piece['brace']]['cb']
				while piece['count']:
					if piece['count'] in currentCbList:
						lastOpeningBrace += 1
						openingBraceStack[lastOpeningBrace] = piece
						break
					
					piece['count'] -= 1
		
		elif found == 'pipe':
			# lets set a title if it is a first separator, or next part otherwise
			if opeingBraceStack[lastOpeningBrace]['parts'] is None:
				openingBraceStack[lastOpeningBrace]['title'] = \
					text[openingBraceStack[lastOpeningBrace]['partStart']:i]
				openingBraceStack[lastOpeningBrace]['parts'] = []
			else:
				openingBraceStack[lastOpeningBrace]['parts'].append(
					text[openingBraceStack[lastOpeningBrace]['partStart']:i]
				)
			i += 1
			openingBraceStack[lastOpeningBrace]['partStart'] = i

	return text

def braceSubstitution(piece):
	"""
	Return the text of a template, after recursively
	replacing any variables or templates within the template.
	"""
#	global $wgContLang, $wgLang, $wgAllowDisplayTitle, $action;

	# Flags
	found = False			 # $text has been filled
	nowiki = False			# wiki markup in $text should be escaped
	noparse = False		   # Unsafe HTML tags should not be stripped, etc.
	noargs = False			# Don't replace triple-brace arguments in $text
	replaceHeadings = False   # Make the edit section links go to the template not the article
	isHTML = False			# text is HTML, armour it against wikitext transformation
	forceRawInterwiki = False # Force interwiki transclusion to be done in raw mode not rendered

	# Title object, where $text came from
	title = None

	linestart = '';

		
	# part1 is the bit before the first |, and must contain only title characters
	# args is a list of arguments, starting from index 0, not including $part1

	titleText = part1 = piece['title']
	# If the third subpattern matched anything, it will start with |

	if piece['parts'] is None:
		replaceWith = variableSubstitution([piece['text'], piece['title']])
		if replaceWith != piece['text']:
			text = replaceWith
			found = True
			noparse = True
			noargs = True
	
	args = piece['parts'] is None and [] or piece['parts']
	argc = len(args)

	# SUBST
	if not found:
		mwSubst = u"SUBST"
		if part1.find(mwSubst) != -1:
			# One of two possibilities is true:
			# 1) Found SUBST but not in the PST phase
			# 2) Didn't find SUBST and in the PST phase
			# In either case, return without further processing
			part1.replace(mwSubst, u'', 1)
			text = piece['text']
			found = True
			noparse = True
			noargs = True

	# MSG, MSGNW and RAW
	if not found:
		# Check for MSGNW:
		mwMsgnw = u"MSGNW"
		if part1.find(mwMsgnw) != -1:
			part1.replace(mwMsgnw, u'', 1)
			nowiki = True
		else:
			mwMsg = u"MSG"
			part1.replace(mwMsg, u'', 1)
		
		# Check for RAW:
		mwRaw = u"RAW"
		if part1.find(mwRaw) != -1:
			part1.replace(mwRaw, u'', 1)
			forceRawInterwiki = True
	
	# Parser functions
	if not found:
		colonPos = part1.find(u':')
		if colonPos != -1:
			# Case sensitive functions
			function = part1[0:colonPos]
			if function in mFunctionSynonyms[1]:
				function = mFunctionSynonyms[1][function]
			else:
				# Case insensitive functions
				function = function.lower()
				if function in mFunctionSynonyms[0]:
					function = mFunctionSynonyms[0][function]
				else:
					function = False
			
			if function:
				funcArgs = [x.strip() for x in args]
				funcArgs += [None, part1[colonPos+1:].strip()]
				result = mFunctionHooks[function](*funcArgs)
				found = True

				# The text is usually already parsed, doesn't need triple-brace tags expanded, etc.
				#$noargs = true;
				#$noparse = true;
				
				if isinstance(result, dict):
					if 0 in result:
						tex = linestart + list[0]
						del list[0]
					
					# Extract flags into the local scope
					# This allows callers to set flags such as nowiki, noparse, found, etc.
					if 'nowiki' in result:
						nowiki = result['nowiki']
					if 'noparse' in result:
						noparse = result['noparse']
					if 'found' in result:
						found = result['found']
				else:
					text = linestart + result

	# Template table test

	# Did we encounter this template already? If yes, it is in the cache
	# and we need to check for loops.
	if not found and piece['title'] in mTemplates:
		found = True

		# Infinite loop test
		if part1 in mTemplatePath:
			noparse = True
			noargs = True
			found = True
			text = linestart + u"[[" + part1 + u"]]<!-- WARNING: template loop detected -->"
		else:
			text = linestart + mTemplates[piece['title']]
	
	# Load from database
	lastPathLevel = mTemplatePath
	if not found:
		ns = NS_TEMPLATE;
		# declaring $subpage directly in the function call
		# does not work correctly with references and breaks
		# {{/subpage}}-style inclusions
		subpage = u''
		part1 = maybeDoSubpageLink(part1, subpage)
		if subpage != u'':
			ns = mTitle.getNamespace()
		title = Title.newFromText(part1, ns)
		
		if title is not None:
			titleText = title.getPrefixedText()
			checkVariantLink = len(wgContLang.getVariants()) > 1
			# Check for language variants if the template is not found
			if checkVariantLink and title.getArticleID() == 0:
				wgContLang.findVariantLink(part1, title)
			if title.isExternal():
				if title.getNamespace() == u"Special" and mOptions.getAllowSpecialInclusion():
					text = SpecialPage.capturePath(title)
					if isinstance(text, basestring):
						found = True
						noparse = True
						noargs = True
						isHTML = True
						this.disableCache()
				else:
					articleContent = fetchTemplate(title)
					if articleContent != False:
						found = True
						text = articleContent
						replaceHeadings = true
				
				# If the title is valid but undisplayable, make a link to it
				if not found:
					text = u"[[:" + titleText + u"]]"
					found = True
			elif title.isTrans():
				pass
#				# Interwiki transclusion
#				if ( $this->ot['html'] && !$forceRawInterwiki ) {
#					$text = $this->interwikiTransclude( $title, 'render' );
#					$isHTML = true;
#					$noparse = true;
#				} else {
#					$text = $this->interwikiTransclude( $title, 'raw' );
#					$replaceHeadings = true;
#				}
#				$found = true;
#			}

			# Template cache array insertion
			# Use the original $piece['title'] not the mangled $part1, so that
			# modifiers such as RAW: produce separate cache entries
			if found:
				if isHTML:
					pass # A special page; don't store it in the template cache.
				else:
					mTemplates[place['title']] = text
				text = linestart + text

#	 if ( $found && !$this->incrementIncludeSize( 'pre-expand', strlen( $text ) ) ) {
#		 # Error, oversize inclusion
#		 $text = $linestart .
#			 "[[$titleText]]<!-- WARNING: template omitted, pre-expand include size too large -->";
#		 $noparse = true;
#		 $noargs = true;
#	 }
# 
#	 # Recursive parsing, escaping and link table handling
#	 # Only for HTML output
#	 if ( $nowiki && $found && ( $this->ot['html'] || $this->ot['pre'] ) ) {
#		 $text = wfEscapeWikiText( $text );
#	 } elseif ( !$this->ot['msg'] && $found ) {
#		 if ( $noargs ) {
#			 $assocArgs = array();
#		 } else {
#			 # Clean up argument array
#			 $assocArgs = array();
#			 $index = 1;
#			 foreach( $args as $arg ) {
#				 $eqpos = strpos( $arg, '=' );
#				 if ( $eqpos === false ) {
#					 $assocArgs[$index++] = $arg;
#				 } else {
#					 $name = trim( substr( $arg, 0, $eqpos ) );
#					 $value = trim( substr( $arg, $eqpos+1 ) );
#					 if ( $value === false ) {
#						 $value = '';
#					 }
#					 if ( $name !== false ) {
#						 $assocArgs[$name] = $value;
#					 }
#				 }
#			 }
# 
#			 # Add a new element to the templace recursion path
#			 $this->mTemplatePath[$part1] = 1;
#		 }
# 
#		 if ( !$noparse ) {
#			 # If there are any <onlyinclude> tags, only include them
#			 if ( in_string( '<onlyinclude>', $text ) && in_string( '</onlyinclude>', $text ) ) {
#				 preg_match_all( '/<onlyinclude>(.*?)\n?<\/onlyinclude>/s', $text, $m );
#				 $text = '';
#				 foreach ($m[1] as $piece)
#					 $text .= $piece;
#			 }
#			 # Remove <noinclude> sections and <includeonly> tags
#			 $text = preg_replace( '/<noinclude>.*?<\/noinclude>/s', '', $text );
#			 $text = strtr( $text, array( '<includeonly>' => '' , '</includeonly>' => '' ) );
# 
#			 if( $this->ot['html'] || $this->ot['pre'] ) {
#				 # Strip <nowiki>, <pre>, etc.
#				 $text = $this->strip( $text, $this->mStripState );
#				 if ( $this->ot['html'] ) {
#					 $text = Sanitizer::removeHTMLtags( $text, array( &$this, 'replaceVariables' ), $assocArgs );
#				 } elseif ( $this->ot['pre'] && $this->mOptions->getRemoveComments() ) {
#					 $text = Sanitizer::removeHTMLcomments( $text );
#				 }
#			 }
#			 $text = $this->replaceVariables( $text, $assocArgs );
# 
#			 # If the template begins with a table or block-level
#			 # element, it should be treated as beginning a new line.
#			 if (!$piece['lineStart'] && preg_match('/^({\\||:|;|#|\*)/', $text)) /*}*/{ 
#				 $text = "\n" . $text;
#			 }
#		 } elseif ( !$noargs ) {
#			 # $noparse and !$noargs
#			 # Just replace the arguments, not any double-brace items
#			 # This is used for rendered interwiki transclusion
#			 $text = $this->replaceVariables( $text, $assocArgs, true );
#		 }
#	 }
#	 # Prune lower levels off the recursion check path
#	 $this->mTemplatePath = $lastPathLevel;
# 
#	 if ( $found && !$this->incrementIncludeSize( 'post-expand', strlen( $text ) ) ) {
#		 # Error, oversize inclusion
#		 $text = $linestart .
#			 "[[$titleText]]<!-- WARNING: template omitted, post-expand include size too large -->";
#		 $noparse = true;
#		 $noargs = true;
#	 }
# 
#	 if ( !$found ) {
#		 wfProfileOut( $fname );
#		 return $piece['text'];
#	 } else {
#		 wfProfileIn( __METHOD__ . '-placeholders' );
#		 if ( $isHTML ) {
#			 # Replace raw HTML by a placeholder
#			 # Add a blank line preceding, to prevent it from mucking up
#			 # immediately preceding headings
#			 $text = "\n\n" . $this->insertStripItem( $text, $this->mStripState );
#		 } else {
#			 # replace ==section headers==
#			 # XXX this needs to go away once we have a better parser.
#			 if ( !$this->ot['wiki'] && !$this->ot['pre'] && $replaceHeadings ) {
#				 if( !is_null( $title ) )
#					 $encodedname = base64_encode($title->getPrefixedDBkey());
#				 else
#					 $encodedname = base64_encode("");
#				 $m = preg_split('/(^={1,6}.*?={1,6}\s*?$)/m', $text, -1,
#					 PREG_SPLIT_DELIM_CAPTURE);
#				 $text = '';
#				 $nsec = 0;
#				 for( $i = 0; $i < count($m); $i += 2 ) {
#					 $text .= $m[$i];
#					 if (!isset($m[$i + 1]) || $m[$i + 1] == "") continue;
#					 $hl = $m[$i + 1];
#					 if( strstr($hl, "<!--MWTEMPLATESECTION") ) {
#						 $text .= $hl;
#						 continue;
#					 }
#					 preg_match('/^(={1,6})(.*?)(={1,6})\s*?$/m', $hl, $m2);
#					 $text .= $m2[1] . $m2[2] . "<!--MWTEMPLATESECTION="
#						 . $encodedname . "&" . base64_encode("$nsec") . "-->" . $m2[3];
# 
#					 $nsec++;
#				 }
#			 }
#		 }
#		 wfProfileOut( __METHOD__ . '-placeholders' );
#	 }
# 
#	 # Prune lower levels off the recursion check path
#	 $this->mTemplatePath = $lastPathLevel;
# 
#	 if ( !$found ) {
#		 wfProfileOut( $fname );
#		 return $piece['text'];
#	 } else {
#		 wfProfileOut( $fname );
#		 return $text;
#	 }
# }

_guillemetLeftPat = re.compile(ur'(.) (\?|:|;|!|\302\273)', re.UNICODE)
_guillemetRightPat = re.compile(ur'(\302\253) ', re.UNICODE)
def fixtags(text):
	"""Clean up special characters, only run once, next-to-last before doBlockLevels"""
	# french spaces, last one Guillemet-left
	# only if there is something before the space
	text = _guillemetLeftPat.sub(ur'\1&nbsp;\2', text)
	# french spaces, Guillemet-right
	text = _guillemetRightPat.sub(ur'\1&nbsp;', text)
	return text

def closeParagraph(mLastSection):
	"""Used by doBlockLevels()"""
	result = u''
	if mLastSection != u'':
		result = u'</' + mLastSection + u'>\n'
	
	return result

def getCommon(st1, st2):
	"""
	getCommon() returns the length of the longest common substring
	of both arguments, starting at the beginning of both.
	"""
	fl = len(st1)
	shorter = len(st2)
	if fl < shorter:
		shorter = fl
	
	i = 0
	while i < shorter:
		if st1[i] != st2[i]:
			break
		i += 1
	return i

def openList(char, mLastSection):
	"""
	These next three functions open, continue, and close the list
	element appropriate to the prefix character passed into them.
	"""
	result = closeParagraph(mLastSection)
	
	mDTopen = False
	if char == u'*':
		result += u'<ul><li>'
	elif char == u'#':
		result += u'<ol><li>'
	elif char == u':':
		result += u'<dl><dd>'
	elif char == u';':
		result += u'<dl><dt>'
		mDTopen = True
	else:
		result += u'<!-- ERR 1 -->'
	
	return result, mDTopen

def nextItem(char, mDTopen):
	if char == u'*' or char == '#':
		return u'</li><li>', None
	elif char == u':' or char == u';':
		close = u'</dd>'
		if mDTopen:
			close = '</dt>'
		if char == u';':
			return close + u'<dt>', True
		else:
			return close + u'<dd>', False
	return u'<!-- ERR 2 -->'

def closeList(char, mDTopen):
	if char == u'*':
		return u'</li></ul>\n'
	elif char == u'#':
		return u'</li></ol>\n'
	elif char == u':':
		if mDTopen:
			return u'</dt></dl>\n'
		else:
			return u'</dd></dl>\n'
	else:
		return u'<!-- ERR 3 -->'

_closePrePat = re.compile(u"</pre", re.UNICODE | re.IGNORECASE)
_openPrePat = re.compile(u"<pre", re.UNICODE | re.IGNORECASE)
_openMatchPat = re.compile(u"(<table|<blockquote|<h1|<h2|<h3|<h4|<h5|<h6|<pre|<tr|<p|<ul|<ol|<li|</center|</tr|</td|</th)", re.UNICODE | re.IGNORECASE)

def doBlockLevels(text, linestart, mUniqPrefix):
	"""Make lists from lines starting with ':', '*', '#', etc."""
	# Parsing through the text line by line.  The main thing
	# happening here is handling of block-level elements p, pre,
	# and making lists from lines starting with * # : etc.
	#
	textLines = text.split(u'\n')
	
	lastPrefix = output = u''
	mDTopen = inBlockElem = False
	prefixLength = 0
	paragraphStack = False
	
	if not linestart:
		output = textLines.pop(0)
	
	mInPre = False
	mLastSection = u''
	mDTopen = False
	
	for oLine in textLines:
		lastPrefixLength = len(lastPrefix)
		preCloseMatch = _closePrePat.search(oLine)
		preOpenMatch = _openPrePat.search(oLine)
		if not mInPre:
			chars = u'*#:;'
			prefixLength = 0
			for c in oLine:
				if c in chars:
					prefixLength += 1
				else:
					break
			pref = oLine[0:prefixLength]
			
			# eh?
			pref2 = pref.replace(u';', u':')
			t = oLine[prefixLength:]
			mInPre = bool(preOpenMatch)
		else:
			# Don't interpret any other prefixes in preformatted text
			prefixLength = 0
			pref = pref2 = u''
			t = oLine

		# List generation
		if prefixLength and lastPrefix == pref2:
			# Same as the last item, so no need to deal with nesting or opening stuff
			tmpOutput, tmpMDTopen = nextItem(pref[-1:], mDTopen)
			output += tmpOutput
			if tmpMDTopen is not None:
				mDTopen = tmpMDTopen
			paragraphStack = False
			
			if pref[-1:] == u';':
				# The one nasty exception: definition lists work like this:
				# ; title : definition text
				# So we check for : in the remainder text to split up the
				# title and definition, without b0rking links.
				term = t2 = u''
				if findColonNoLinks(t, term, t2) != False:
					t = t2
					output += term
					tmpOutput, tmpMDTopen = nextItem(u':', mDTopen)
					output += tmpOutput
					if tmpMDTopen is not None:
						mDTopen = tmpMDTopen
		
		elif prefixLength or lastPrefixLength:
			# Either open or close a level...
			commonPrefixLength = getCommon(pref, lastPrefix)
			paragraphStack = False
			
			while commonPrefixLength < lastPrefixLength:
				tmp = closeList(lastPrefix[lastPrefixLength-1], mDTopen)
				output += tmp
				mDTopen = False
				lastPrefixLength -= 1
			if prefixLength <= commonPrefixLength and commonPrefixLength > 0:
				tmpOutput, tmpMDTopen = nextItem(pref[commonPrefixLength-1])
				output += tmpOutput
				if tmpMDTopen is not None:
					mDTopen = tmpMDTopen
			
			while prefixLength > commonPrefixLength:
				char = pref[commonPrefixLength:commonPrefixLength+1]
				tmpOutput, tmpMDTOpen = openList(char, mLastSection)
				if tmpMDTOpen:
					mDTopen = True
				output += tmpOutput
				mLastSection = u''
				mInPre = False
				
				if char == u';':
					# FIXME: This is dupe of code above
					if findColonNoLinks(t, term, t2) != False:
						t = t2
						output += term
						tmpOutput, tmpMDTopen = nextItem(u':', mDTopen)
						output += tmpOutput
						if tmpMDTopen is not None:
							mDTopen = tmpMDTopen
				
				commonPrefixLength += 1
			
			lastPrefix = pref2
		
		if prefixLength == 0:
			# No prefix (not in list)--go to paragraph mode
			# XXX: use a stack for nestable elements like span, table and div
			openmatch = _openMatchPat.search(t)
			_closeMatchPat = re.compile(ur"(</table|</blockquote|</h1|</h2|</h3|</h4|</h5|</h6|<td|<th|<div|</div|<hr|</pre|</p|" +  mUniqPrefix + ur"-pre|</li|</ul|</ol|<center)", re.UNICODE | re.IGNORECASE)
			closematch = _closeMatchPat.search(t)
			if openmatch or closematch:
				paragraphStack = False
				output += closeParagraph(mLastSection)
				mLastSection = u''
				mInPre = False
				if preOpenMatch and not preCloseMatch:
					mInPre = True
				if closematch:
					inBlockElem = False
				else:
					inBlockElem = True
			elif not inBlockElem and not mInPre:
				if t[0:1] == u' ' and (mLastSection ==  u'pre' or t.strip() != u''):
					# pre
					if mLastSection != u'pre':
						paragraphStack = False
						output += closeParagraph(u'') + u'<pre>'
						mInPre = False
						mLastSection = u'pre'
					t = t[1:]
				else:
					# paragraph
					if t.strip() == u'':
						if paragraphStack:
							output += paragraphStack + u'<br />'
							paragraphStack = False
							mLastSection = u'p'
						else:
							if mLastSection != u'p':
								output += closeParagraph(mLastSection)
								mLastSection = u''
								mInPre = False
								paragraphStack = u'<p>'
							else:
								paragraphStack = u'</p><p>'
					else:
						if paragraphStack:
							output += paragraphStack
							paragraphStack = False
							mLastSection = u'p'
						elif mLastSection != u'p':
							output += closeParagraph(mLastSection) + u'<p>'
							mLastSection = u'p'
							mInPre = False
		
		# somewhere above we forget to get out of pre block (bug 785)
		if preCloseMatch and mInPre:
			mInPre = False
		
		if paragraphStack == False:
			output += t + u"\n"
	
	while prefixLength:
		output += closeList(pref2[prefixLength-1], mDTopen)
		mDTopen = False
		prefixLength -= 1
	
	if mLastSection != u'':
		output += u'</' + mLastSection + u'>'
		mLastSection = u''
	
	return output

def parse(text, showToc=True):
	"""docstring for parse"""
	utf8 = isinstance(text, str)
	text = to_unicode(text)
	if text[-1:] != u'\n':
		text = text + u'\n'
		taggedNewline = True
	else:
		taggedNewline = False
	mStripState = {}
	mUniqPrefix = u"\x07UNIQ" + unicode(random.randint(1, 1000000000))

	text = strip(text, mStripState, mUniqPrefix)
	text = removeHtmlTags(text)
	text = replaceVariables(text)
	text = doTableStuff(text, mStripState)
	text = parseHorizontalRule(text)
	text, toc = checkTOC(text)
	text = parseHeaders(text)
	text = parseAllQuotes(text)
	text = replaceInternalLinks(text)
	text = replaceExternalLinks(text)
	if not toc and text.find(u"<!--MWTOC-->") == -1:
		showToc = False
	text = formatHeadings(text, True, showToc, mStripState)
	text = unstrip(text, mStripState)
	text = fixtags(text)
	text = doBlockLevels(text, True, mUniqPrefix)
	text = unstripNoWiki(text, mStripState)
	if taggedNewline and text[-1:] == u'\n':
		text = text[:-1]
	if utf8:
		return text.encode("utf-8")
	return text

def truncate_url(url, length=40):
	if len(url) <= length:
		return url
	import re
	pattern = r'(/[^/]+/?)$'
	match = re.search(pattern, url)
	if not match:
		return url
	l = len(match.group(1))
	domain = url.replace(match.group(1), '')
	firstpart = url[0:len(url)-l]
	secondpart = match.group(1)
	if firstpart == firstpart[0:length-3]:
		secondpart = secondpart[0:length-3] + '...'
	else:
		firstpart = firstpart[0:length-3]
		secondpart = '...' + secondpart
	t_url = firstpart+secondpart
	return t_url
	
def to_unicode(text, charset=None):
	"""Convert a `str` object to an `unicode` object.

	If `charset` is given, we simply assume that encoding for the text,
	but we'll use the "replace" mode so that the decoding will always
	succeed.
	If `charset` is ''not'' specified, we'll make some guesses, first
	trying the UTF-8 encoding, then trying the locale preferred encoding,
	in "replace" mode. This differs from the `unicode` builtin, which
	by default uses the locale preferred encoding, in 'strict' mode,
	and is therefore prompt to raise `UnicodeDecodeError`s.

	Because of the "replace" mode, the original content might be altered.
	If this is not what is wanted, one could map the original byte content
	by using an encoding which maps each byte of the input to an unicode
	character, e.g. by doing `unicode(text, 'iso-8859-1')`.
	"""
	if not isinstance(text, str):
		if isinstance(text, Exception):
			# two possibilities for storing unicode strings in exception data:
			try:
				# custom __str__ method on the exception (e.g. PermissionError)
				return unicode(text)
			except UnicodeError:
				# unicode arguments given to the exception (e.g. parse_date)
				return ' '.join([to_unicode(arg) for arg in text.args])
		return unicode(text)
	if charset:
		return unicode(text, charset, 'replace')
	else:
		try:
			return unicode(text, 'utf-8')
		except UnicodeError:
			return unicode(text, locale.getpreferredencoding(), 'replace')
