#!/usr/bin/python

from optparse import OptionParser
import sys
import os

try:
    import settings
except ImportError:
    print "Settings file not found.  Place this file in the same place as manage.py"
    sys.exit()

project_directory = os.path.dirname(settings.__file__)
project_name = os.path.basename(project_directory)
sys.path.append(os.path.join(project_directory, '..'))
project_module = __import__(project_name, '', '', [''])
sys.path.pop()
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % project_name

from django.db import models
from django.template import Context, Template

p = OptionParser()

p.add_option("-a", "--app", dest="app", help="The app which contains the model")
p.add_option("-m", "--model", dest="model", help="The model to produce the form for")

options, args = p.parse_args()

if not (options.model and options.app):
    p.print_help()
    sys.exit()

m = __import__("%s.%s.models" % (project_name, options.app,), '', '', [options.model])

a = getattr(m, options.model)

def image_field_html(name):
    return '''\
        {{ form.NAME_file }} \
        {{ form.NAME }}
        {% if form.NAME.errors %}
        *** {{ form.NAME.errors|join:", " }}
        {% endif %}'''.replace('NAME', name)

def field_html(name):
    return '''\
    {{ form.NAME }}
    {% if form.NAME.errors %}
      *** {{ form.NAME.errors|join:", " }}
    {% endif %}'''.replace('NAME', name)


def labeled_field_html(field):
    if isinstance(field, models.DateTimeField):
        rows = [field_html(field.name + '_' + suffix)
                for suffix in 'date', 'time']
    elif isinstance(field, models.ImageField):
        rows = [image_field_html(field.name)]
    else:
        rows = [field_html(field.name)]
    return '''\
  <p>
    <label for="id_%s">%s:</label>
%s
  </p>''' % (field.name, field.verbose_name or field.name, '\n'.join(rows))


#print '<form method="POST" action=".">'
#print '\n'.join(labeled_field_html(f) for f in a._meta.fields if f.name !='id')
#print '  <input type="submit" value="submit" />'
#print '</form>'

template = Template(
"""<form method="POST" action=".">
{{ formfields }}
<input type="submit" value="submit" />
</form>
""")

context = Context({'formfields': '\n'.join(labeled_field_html(f) for f in a._meta.fields + a._meta.many_to_many if f.name !='id')})
print template.render(context)
