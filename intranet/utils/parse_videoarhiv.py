#!/usr/bin/python

from BeautifulSoup import BeautifulSoup

import urllib

def parse_video(video):    
  results = {'thumb': video.find('img', {'class':'thumb'}).get('src', None),
             'title': video.find('a', {'class':'title'}).contents,
             'url': video.find('a', {'class':'title'}).get('href', None),
             'author': video.find('div', {'class':'videoinfo'}).findAll('p')[1].contents[0].split(' &bull;')[0],
             'date': video.find('div', {'class':'videoinfo'}).findAll('p')[1].contents[1].contents,
             'intranet-id': None,
            }

  #lets get intranet-id from info.txt now
  
  info_url = 'http://video.kiberpipa.org' + results.get('url')[:-9] + 'info.txt'
  
  f = urllib.urlopen(info_url)
  
  for line in f.readlines():
    if 'intranet-id' in line:
      results['intranet-id'] = line.split()[1]
  
  return results

def main():
  
  f = urllib.urlopen('http://video.kiberpipa.org/vse.html')
  soup = BeautifulSoup(f.read())
  f.close()
  
  video_list = []
  for video in soup.findAll('td', {'class':'video right'}):
    video_list.append(video)

  for video in soup.findAll('td', {'class':'video left'}):
    video_list.append(video)
  
  parsed_video_list = list()
  for video in video_list:
    parsed_video_list.append(parse_video(video))
    
  print parsed_video_list
  
if __name__ == '__main__':
  main()
