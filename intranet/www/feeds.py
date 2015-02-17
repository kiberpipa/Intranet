# *-* coding: utf-8 *-*
import datetime

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from feedjack.models import Post

from intranet.org.models import Event, Project
from intranet.www.models import News


class MediaRssFeed(Rss201rev2Feed):
    """
    Implement thumbnails which adhere to Yahoo Media RSS (mrss) feed.

    @see http://djangosnippets.org/snippets/1648/
    """
    def rss_attributes(self):
        attrs = super(MediaRssFeed, self).rss_attributes()
        attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        return attrs

    def add_item_elements(self, handler, item):
        """
        Callback to add thumbnail element to each item (item/entry) element.
        """
        super(MediaRssFeed, self).add_item_elements(handler, item)

        if item.get('thumbnail_url') != None:

            thumbnail = { 'url': item['thumbnail_url'] }

            if 'thumbnail_width' in item:
                thumbnail['width'] = str(item['thumbnail_width'])

            if 'thumbnail_height' in item:
                thumbnail['height'] = str(item['thumbnail_height'])

            handler.addQuickElement(u"media:thumbnail", '', thumbnail)


class NewsFeed(Feed):
    title = "Kiberpipa - Novice"
    link = "/sl/feeds/novice/"
    description = "Novice"
    feed_type = MediaRssFeed

    def items(self):
        return News.objects.order_by('-date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text  # safe

    def item_pubdate(self, item):
        return item.date

    def item_extra_kwargs(self, item):
        """
        Return a dictionary to the feedgenerator for each item to be added to the feed.
        If the object is a Gallery, uses a random sample image for use as the feed Item
        """
        try:
            return {
                'thumbnail_url': item.image.url,
            }
        except ValueError:
            return { }


class EventsFeed(Feed):
    title = "Kiberpipa - Dogodki"
    link = "/sl/feeds/dogodki/"
    description = "Najave dogodkov v Kiberpipi"
    feed_type = MediaRssFeed

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

    def item_pubdate(self, item):
        return item.start_date if hasattr(item, "start_date") else item.date

    def item_extra_kwargs(self, item):
        """
        Return a dictionary to the feedgenerator for each item to be added to the feed.
        If the object is a Gallery, uses a random sample image for use as the feed Item
        """

        return {
            'thumbnail_url': item.event_image.image.url,
            # Optional
            # 'thumbnail_width': 480,
            # 'thumbnail_height': 250,
        }


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
