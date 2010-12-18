#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flickrapi
from django.conf import settings
from django.utils import simplejson
from django.template import Node, Library, loader

register = Library()


class PhotosBoxNode(Node):
    def __init__(self):
        pass

    def render(self, context):
        flickr_set_id = context['event'].flickr_set_id
        if not flickr_set_id:
            return ''

        api = flickrapi.FlickrAPI(
                settings.PHOTOS_FLICKR_APIKEY,
                settings.PHOTOS_FLICKR_SECRET,
                token=settings.PHOTOS_FLICKR_TOKEN,
                )

        r = api.flickr_call(
                method='flickr.photosets.getPhotos',
                photoset_id=flickr_set_id,
                format="json",
                nojsoncallback=1)

        images = []
        json = simplejson.loads(r)
        for image in json['photoset']['photo']:
            image['thumb_url'] = settings.PHOTOS_FLICKR_IMAGE_URL_S % image
            image['url'] = settings.PHOTOS_FLICKR_IMAGE_URL % image
            images.append(image)
        t = loader.get_template('gallery/photos_box.html')
        context['images'] = images
        return t.render(context)


def photos_box(parser, token):
    return PhotosBoxNode()

photos_box = register.tag('photos_box', photos_box)
