# *-* coding: utf-8 *-*
import datetime

from django.contrib.syndication.views import Feed
from feedjack.models import Post

from intranet.org.models import Event, Project
from intranet.www.models import News


class NewsFeed(Feed):
    title = "Kiberpipa - Novice"
    link = "/sl/feeds/novice/"
    description = "Novice"

    def items(self):
        return News.objects.order_by('-date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text  # safe


class EventsFeed(Feed):
    title = "Kiberpipa - Dogodki"
    link = "/sl/feeds/dogodki/"
    description = "Najave dogodkov v Kiberpipi"

    def _get_events(self):
        return Event.objects.filter(public=True, start_date__lte=datetime.datetime.today() + datetime.timedelta(8)).order_by('-start_date')

    def items(self):
        return self._get_events()[:10]

    def item_title(self, item):
        if getattr(item, 'project', None):
            return u"%s: %s" % (item.project, item.title)
        else:
            return item.title

    def item_description(self, item):
        return item.announce  # safe


class POTFeed(EventsFeed):
    title = "Kiberpipa - POT"
    link = "/sl/feeds/pot/"
    description = "Pipini odprti termini"

    def items(self):
        return self._get_events().filter(project=Project.objects.get(pk=1))[:10]


class SUFeed(EventsFeed):
    title = "Kiberpipa - Spletne Urice"
    link = "/sl/feeds/su/"
    description = "Spletne urice"

    def items(self):
        return self._get_events().filter(project=Project.objects.get(pk=6))[:10]


class VIPFeed(EventsFeed):
    title = u"Kiberpipa - Večeri za inovativne in podjetne"
    link = "/sl/feeds/vip/"
    description = u"Večeri za inovativne in podjetne"

    def items(self):
        return self._get_events().filter(project=Project.objects.get(pk=14))[:10]


class PlanetFeed(Feed):
    title = "Planet Kiberpipa"
    link = "/sl/feeds/planet/"
    description = "Planet Kiberpipa"

    def items(self):
        return Post.objects.order_by('-date_modified')[:10]

    def item_description(self, item):
        return item.content  # safe


class MuzejFeed(Feed):
    title = "Kiberpipin računalniški muzej"
    link = "/sl/feeds/muzej/"
    description = "Kiberpipin računalniški muzej"

    def items(self):
        return Post.objects.filter(feed=12).order_by('-date_modified')[:10]

    def item_description(self, item):
        return item.content  # safe


class AllInOne(EventsFeed):
    title = "Kiberpipa - vse"
    link = '/sl/feeds/all/'
    description = "Vsa dogajanja v Kiberpipi"

    def items(self):
        events = [(e.start_date, e) for e in self._get_events()[:10]]
        news = [(n.date, n) for n in News.objects.order_by('-date')[:10]]
        items = events + news
        items.sort()
        items.reverse()
        return [f for d, f in items]

    def item_description(self, item):
        return getattr(item, 'text', '') + getattr(item, 'announce', '') + getattr(item, 'content', '')  # safe
