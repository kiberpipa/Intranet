import datetime

from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from intranet.org.models import Event, Project
#from intranet.photologue.models import Gallery
from intranet.www.models import News
from intranet.feedjack.models import Post

class AllInOne(Feed):
    def __init__(self, slug, request):
        #painfully slow, cache me!!
        Feed.__init__(self, slug, request)
        
        bits = request.path.split('/')

        today = datetime.datetime.today()
        push = datetime.timedelta(2)

        events = Event.objects.filter(public=True, start_date__lte=today + push)
        
        pot = [(e.start_date-push, e) for e in events.filter(project=Project.objects.get(pk=1)).order_by('-start_date')[:10]]
        su = [(e.start_date-push, e) for e in events.filter(project=Project.objects.get(pk=6)).order_by('-start_date')[:10]]
        vip = [(e.start_date-push, e) for e in events.filter(project=Project.objects.get(pk=14)).order_by('-start_date')[:10]]
        events = [(e.start_date-push, e) for e in events.order_by('-start_date')[:10]]
        news =  [(n.date, n) for n in News.objects.order_by('-date')[:10]]
        #albums =  [(g.date_added, g) for g in Gallery.objects.order_by('-date_added')[:10]]
        planet =  [(p.date_modified, p) for p in Post.objects.order_by('-date_modified')[:10]]
        muzej =  [(p.date_modified, p) for p in Post.objects.filter(feed=12).order_by('-date_modified')[:10]]

    

        feeds = {
            'events': events,
            'planet': planet,
            'news': news,
            #'albums': albums,
            'pot': pot,
            'su': su,
            'vip': vip,
            'muzej': muzej,
            #'all': events + news + albums + pot + su + muzej,
            'all': events + news + pot + su + muzej,
        }

        items = []
        new_bits = []
        for b in bits:
            if b:
                new_bits.append(b)
        del new_bits[0:2]

        for i in new_bits:
            items.extend(feeds[i])

        items.sort()
        items.reverse()
        self.items = []
        for date, feed in items:
            if feed not in self.items:
                self.items.append(feed)
        

        self.title = ' | '.join(new_bits)
        self.link = request.path

    def items(self):
        return self.items

    def item_link(self, obj):
        if isinstance(obj, Event):
            return obj.get_public_url()
        else:
            return obj.get_absolute_url()
