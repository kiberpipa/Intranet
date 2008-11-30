#!/usr/bin/env python
import sys
import datetime
import simplejson
from urllib2 import urlopen

from django.conf import settings 

from intranet.org.models import Event, Sodelovanje
import twitter

api = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
today = datetime.datetime.today()
events = Event.objects.filter(start_date__year=today.year, start_date__month=today.month, start_date__day=today.day)
try:
    sys.argv[1]
    #the announce event tweet
    for e in events:
        url = e.get_public_url()
        dump = urlopen('http://api.bit.ly/shorten?version=2.0.0&long_url=' + url +'&login=crkn&api_key=R_678ce6a3bba1c3f64f996080e21909c2')
        short_url = simplejson.loads(dump.read())['results'][url]['hashUrl']
        if Sodelovanje.objects.filter(event=e).count() == 1:
            sodelovanja = '- ' + Sodelovanje.objects.filter(event=e)[0].person.name
        else:
            sodelovanja = ''
        if e.language == 'SI':
            api.PostUpdate(u'%s danes ob %s:%s #Kiberpipa: %s %s %s' % (e.project, e.start_date.hour, e.start_date.minute, e.title, sodelovanja, short_url))
        else:
            api.PostUpdate(u'%s today at %s:%s #Kiberpipa: %s %s %s' % (e.project, e.start_date.hour, e.start_date.minute, e.title, sodelovanja, short_url))
except IndexError:
    #the live stream announcement
    min_15 = today + datetime.timedelta(seconds=15*60)
    events = events.filter(require_video=True, start_date__range=(today, min_15))
    for e in events:
        url = e.get_public_url()
        dump = urlopen('http://api.bit.ly/shorten?version=2.0.0&long_url=' + url +'&login=crkn&api_key=R_678ce6a3bba1c3f64f996080e21909c2')
        short_url = simplejson.loads(dump.read())['results'][url]['hashUrl']
        if Sodelovanje.objects.filter(event=e).count() == 1:
            sodelovanja = Sodelovanje.objects.filter(event=e)[0].person.name + ' '
        else:
            sodelovanja = ''
        if e.language == 'EN':
            api.PostUpdate(u'%slive from #Kiberpipa (%s: %s): at http://bit.ly/FdgZ' % (sodelovanja, unicode(e.project), e.title))
        else:
            api.PostUpdate(u'%sv zivo iz #Kiberpipa (%s: %s): na http://bit.ly/FdgZ' % (sodelovanja, unicode(e.project), e.title))
