import datetime
from dateutil.relativedelta import relativedelta
import re
from BeautifulSoup import BeautifulSoup, Comment

from django.template import Library
register = Library()

def calclass(date):
    today = datetime.date.today()

    # calculate start of next month, and end of previous month
    next_month = date + relativedelta(months=1)
    next_month = datetime.date(next_month.year, next_month.month, 1)
    prev_month = datetime.date(date.year, date.month, 1) - relativedelta(days=1)

    if date == today:
        return 'koledar-today'
    elif date >= next_month:
        return 'koledar-next'
    elif date <= prev_month:
        return 'koledar-prev  %s vs %s' % (date, prev_month)
    elif date < today:
        return 'koledar-past  %s vs %s' % (date, prev_month)
    elif date > today:
        return 'koledar-future'

    return ''



def sanitize_html(value):
    #valid_tags = 'p i strong b u a h1 h2 h3 pre br img'.split()
    #valid_attrs = 'href src'.split()
    soup = BeautifulSoup(value, convertEntities=BeautifulSoup.HTML_ENTITIES)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        #if tag.name not in valid_tags:
        tag.hidden = True
        #tag.attrs = [(attr, val) for attr, val in tag.attrs
                     #if attr in valid_attrs]
    return soup.renderContents().decode('utf8').replace('javascript:', '')

register.filter('sanitize', sanitize_html)


register.simple_tag(calclass)

# truncate after a certain number of characters
@register.filter
def truncchar(value, arg):
    if len(value) < int(arg):
        return value
    else:
        return value[:int(arg)] + '...'

@register.filter
def spam(value):
    return re.sub('(?P<user>.*)@(?P<domain>.*)', '\g<user>REMOVE@ME\g<domain>', value)
