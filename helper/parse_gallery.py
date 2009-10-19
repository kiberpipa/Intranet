# -*- coding: utf-8 -*-
# easy_install http://pypi.python.org/packages/source/p/phpserialize/phpserialize-1.2.zip
from phpserialize import *
import sys
try:
   import cPickle as pickle
except:
   import pickle


import os
from os.path import join, getsize
from pprint import pprint

dd = list()
for root, dirs, files in os.walk('../../gallery'):
  album_dict = dict()
  
  if 'photos.dat' in files:
    album_dict['dir'] = root
    
    album = loads(open(root+'/album.dat').read(), object_hook=phpobject)
    album_dict['title'] = album.fields.get('title')
    
    album_dict['images'] = list()
    
    images = loads(open(root+'/photos.dat').read(), object_hook=phpobject)
    if images:
      for i in images:
        if images[i].image:
          album_dict['images'].append({'name': "%s.%s" % (images[i].image.name, images[i].image.type),
                   'caption': images[i].caption})

    dd.append(album_dict)


sys.path.append('/home/gandalf/intranet/intranet')
sys.path.append('/home/gandalf/intranet/libs/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'intranet.settings'
from photologue.models import Gallery, Photo
from django.template.defaultfilters import slugify
from time import time

for a in dd:
  print a['dir'].replace('../../gallery/','')
  g = Gallery(title=a['dir'].replace('../../gallery/','').replace('\x9e', 'z').replace('\xbe', 'c').replace('\x8a', 'S').replace('\x9a', 's').replace('\x9e', 'z'),
              title_slug=slugify(a['dir'].replace('../../gallery/','').replace('\x9e', 'z').replace('\xbe', 'c').replace('\x8a', 'S').replace('\x9a', 's').replace('\x9e', 'z'))[:49],
              description=a['title']
              )
  g.save()
  
  for image in a['images']:
    print image, slugify(image['name'])[:90]
    p = Photo(title="%10.15f" % time(),
              title_slug=slugify("%10.15f" % time()),
              image=a['dir'].replace('../../gallery/','').replace('\x8a', 'S')+'/'+image['name'],
              caption=image['caption'].replace('\xbe', 'c').replace('\xf0', '').replace('\xe6', 'c').replace('\xae', '').replace('\x8a', 'S'))
    p.save()
    
    g.photos.add(p)

#f = open('gallery_full.pickle', 'w').write(pickle.dumps(dd))