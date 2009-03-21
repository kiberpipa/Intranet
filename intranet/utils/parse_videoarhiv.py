#!/usr/bin/python

from BeautifulSoup import BeautifulSoup

import urllib
import re
import datetime

from django.core.mail import send_mail

from intranet.www.models import Video
from intranet.org.models import Event

def parse_video(video):    
  ddate = video.find('div', {'class':'videoinfo'}).findAll('p')[1].contents[1].contents[0].split(' ')[0].split('.')
  tdate = datetime.date(int(ddate[2]), int(ddate[1]), int(ddate[0]))

  url = video.find('a', {'class':'title'}).get('href', None)
  results = {'thumb': url[:-9] + 'image-t.jpg',
             'title': video.find('a', {'class':'title'}).contents,
             'url': url,
             'author': video.find('div', {'class':'videoinfo'}).findAll('p')[1].contents[0].split(' &bull;')[0],
             'date': tdate,
             'intranet-id': None,
            }

  #lets get intranet-id from info.txt now
  
  info_url = 'http://video.kiberpipa.org' + results.get('url')[:-9] + 'info.txt'
  results['videodir'] = re.sub('/media/(?P<dir>.*)/.*', '\g<dir>', results.get('url'))
  
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
    
  for i in parsed_video_list:
    try: 
        Video.objects.get(videodir=i['videodir'])
    except Video.DoesNotExist:
        video = Video.objects.create(videodir=i['videodir'],
          #image_url = 'http://video.kiberpipa.org' + i['thumb'], 
          image_url = i['thumb'], 
          pub_date = i['date'], 
          play_url = 'http://video.kiberpipa.org' + i['url'],)

        if i['intranet-id']:
            event = Event.objects.get(pk=i['intranet-id'])
            video.event = event
            video.save()
            subject = 'Posnetek predavanja %s je na voljo' % event.title[:30]
            body = 'Predavanje %s, %s je sedaj na voljo za ogled v Kiberpipinem spletnem arhivu.\n\nOgledate si ga lahko na %s\n\nEkipa Kiberpipe' % (event.title, 'avtor', video.play_url)

            send_mail(subject, body, 'obvestila@kiberpipa.org', [i.email for i in event.emails.all()], fail_silently=True)

  
if __name__ == '__main__':
  main()
