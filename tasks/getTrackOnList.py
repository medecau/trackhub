#Kopimi -- No license.

from google.appengine.api import urlfetch
from google.appengine.api import memcache

api_url='http://track-on.appspot.com/api/live'

result = urlfetch.fetch(api_url)
if result.status_code==200:
  trackers=result.content.split('\n')
  while trackers.count('')>0:
    trackers.remove('')
  if trackers.count('http://trackhub.appspot.com/announce')>0:
    trackers.remove('http://trackhub.appspot.com/announce')
  if trackers.count('https://trackhub.appspot.com/announce')>0:
    trackers.remove('https://trackhub.appspot.com/announce')
  for tracker in trackers:
    if tracker[:5] == 'https':
      if trackers.count(tracker.replace('https','http'))>0:
        trackers.remove(tracker.replace('https','http'))
          
  trackers.sort()
  memcache.set('trackers_list', trackers)