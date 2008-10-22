from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from intranet.org.models import Event
from intranet.photologue.models import Gallery
from intranet.www.models import News

class AllInOne(Feed):
    def __init__(self, slug, request):
        Feed.__init__(self, slug, request)
        
        feed = request.path
        bits = feed.split('/')
        feeds = { 'events': [(e.start_date, e) for e in Event.objects.filter(public=True).order_by('-start_date')[:15]],
            'news': [(n.date, n) for n in News.objects.order_by('-date')[:15]],
            'albums': [(g.date_added, g) for g in Gallery.objects.order_by('-date_added')[:15]],
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
        self.items = [feed for date, feed in items]

        self.title = 'crkn'
        self.description = 'crkn'
        self.link = '/blog/crkn'
    def items(self):
        return self.items
