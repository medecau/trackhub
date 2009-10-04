#Kopimi -- No license.

from google.appengine.api import urlfetch
from google.appengine.api import memcache

self_domain='trackhub.appspot.com'
api_url='http://track-on.appspot.com/api/live'

result = urlfetch.fetch(api_url)
if result.status_code==200:
  trackers=result.content.split('\n') # FUCK XML!
  while trackers.count('')>0:  #
    trackers.remove('')        # REMOVE EMPTY LINES FROM THE LIST
    
  while trackers.count('http://'+self_domain+'/announce')>0:   #
    trackers.remove('http://'+self_domain+'/announce')         #
  while trackers.count('https://'+self_domain+'/announce')>0:  #
    trackers.remove('https://'+self_domain+'/announce')        # REMOVE SELF FROM THE LIST TO AVOID REDIRECT LOOP
    
  for tracker in trackers:                                     #
    if tracker[:5] == 'https':                                 #
      while trackers.count(tracker.replace('https','http'))>0: #
        trackers.remove(tracker.replace('https','http'))       # REMOVE DUAL ENTRANCE TRACKERS
          
  trackers.sort()
  memcache.set('trackers_list', trackers)