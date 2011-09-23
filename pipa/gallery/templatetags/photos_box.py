#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import urllib2

import flickrapi
from django.core.cache import cache
from django.conf import settings
from django.utils import simplejson
from django.template import Node, Library, loader


logger = logging.getLogger(__name__)
register = Library()

api = flickrapi.FlickrAPI(
        settings.PHOTOS_FLICKR_APIKEY,
        settings.PHOTOS_FLICKR_SECRET,
        token=settings.PHOTOS_FLICKR_TOKEN,
        cache=True,
        )
api.cache = cache


class PhotosBoxNode(Node):
    def __init__(self):
        pass

    def render(self, context):
        flickr_set_id = context['event'].flickr_set_id
        if not flickr_set_id:
            return ''

        try:
            r = api.flickr_call(
                method='flickr.photosets.getPhotos',
                photoset_id=flickr_set_id,
                format="json",
                nojsoncallback=1)
        except urllib2.URLError:
            # probably flickr is down or glitch in connection
            return ""

        images = []
        json = simplejson.loads(r)

        if json.get('stat', 'error') == 'ok':
            for image in json['photoset']['photo']:
                image['thumb_url'] = settings.PHOTOS_FLICKR_IMAGE_URL_S % image
                image['url'] = settings.PHOTOS_FLICKR_IMAGE_URL % image
                image['title'] = image.get('title', '')
                images.append(image)
            t = loader.get_template('gallery/photos_box.html')
            context['images'] = images
            return t.render(context)
        else:
            logger.error('Could not fetch images from Flickr', exc_info=True, extra=locals())
            return ''


def photos_box(parser, token):
    return PhotosBoxNode()

photos_box = register.tag('photos_box', photos_box)
