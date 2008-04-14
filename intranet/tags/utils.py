# -*- coding:utf-8 -*-
import re

def normalize_title(title):
  '''
  Casts strings to a representation suitable for searching
  stripping out details insignificant for comparision.
  
  This function has a sibling in js/tags.js, don't forget to 
  update it whenever this function is changed.
  '''
  title=title.decode('utf-8')
  title=title.lower()
  title=title.replace(u'ё',u'е')
  safe_title = title # safe_title can't be empty since nothing has been removed yet
  title=re.sub(re.compile(r'\bthe\b',re.I),'',title)
  title=re.sub(re.compile(r'[\,\.\(\)\-\!\'\"\`\?\_\:\;\$\]\[\#\/]'),'',title)
  title=re.sub(re.compile(r'\s+'),'',title)
  return (title or safe_title).encode('utf-8')