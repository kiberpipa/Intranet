import datetime
import re

from django.template import Library
register = Library()

def calclass(date):
    today = datetime.date.today()
    num_next_month = today - datetime.timedelta(30)
    num_prev_month = today + datetime.timedelta(30)
    next_month = datetime.date(today.year, num_next_month.month, 1)
    prev_month = datetime.date(today.year, num_prev_month.month, 1)

    if date == today:
        return 'koledar-today'
    elif date >= next_month:
        return 'koledar-next'
    elif date <= prev_month:
        return 'koledar-prev'
    elif date < today:
        return 'koledar-past'
    elif date > today:
        return 'koledar-future'

    return ''



def sanitize_html(value):
    try:
        from BeautifulSoup import BeautifulSoup, Comment
    except ImportError:
        return value
    #valid_tags = 'p i strong b u a h1 h2 h3 pre br img'.split()
    #valid_attrs = 'href src'.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        #if tag.name not in valid_tags:
        tag.hidden = True
        #tag.attrs = [(attr, val) for attr, val in tag.attrs
                     #if attr in valid_attrs]
    return soup.renderContents().decode('utf8').replace('javascript:', '')

register.filter('santize', sanitize_html)


register.simple_tag(calclass)

# truncate after a certain number of characters
@register.filter
def truncchar(value, arg):
    if len(value) < arg:
        return value
    else:
        return value[:int(arg)] + '...'

@register.filter
def spam(value):
   return re.sub('(?P<user>.*)@(?P<domain>.*)', '\g<user>REMOVE@ME\g<domain>', value)
