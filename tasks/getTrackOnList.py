#Kopimi -- No license.

from google.appengine.api import urlfetch
from google.appengine.api import memcache

api_url='http://trackon.org/api/live'

result = urlfetch.fetch(api_url)
if result.status_code==200:
  trackers=result.content.split('\n')
  while trackers.count('')>0:
    trackers.remove('')
  trackers.sort()
  memcache.set('trackers_list', trackers)