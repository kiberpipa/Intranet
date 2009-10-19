# easy_install http://pypi.python.org/packages/source/p/phpserialize/phpserialize-1.2.zip
from phpserialize import *
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
    

f = open('gallery_full.pickle', 'w').write(pickle.dumps(dd))