import datetime

from django.template import Library
register = Library()

def calclass(date):
    today = datetime.date.today()
    next_month = datetime.date(today.year, today.month+1, 1)
    prev_month = datetime.date(today.year, today.month-1, 1)

    if date == today:
        return 'today'
    elif date >= next_month:
        return 'next'
    elif date <= prev_month:
        return 'prev'
    elif date < today:
        return 'past'
    elif date > today:
        return 'future'

    return ''


register.simple_tag(calclass)
