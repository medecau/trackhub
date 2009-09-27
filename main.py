#Kopimi -- No license.

import wsgiref.handlers
import re
from google.appengine.ext import webapp
from google.appengine.api import memcache
from trackers_handler import TrackersHandler


## LOCAL CACHING

tHandler = TrackersHandler()
cache_max_age=300
trackers_list = memcache.get('trackers_list')
cache_reset_time=0
redirect_cache={}
info_hash_pattern=re.compile(r".*info_hash=([^?]+).*")


def pick_tracker (self, scrape=False): #CHOOSE ONE TRACKER
  import time
  global tHandler, cache_max_age, trackers_list, cache_reset_time, redirect_cache, info_hash_pattern
    
  # GET THE INT VALUE OF THE FIRST BYTE FROM THE HASH INFO 
  import urllib
  urlencoded_info_hash=info_hash_pattern.match(self.request.query_string).group(1)
  first_char = ord(urllib.unquote(urlencoded_info_hash)[:1])
    
  try: # TRY TO GET THE PICK FROM LOCAL MEMORY CACHE
    tracker=redirect_cache[str(first_char)]
  except:
    if trackers_list is None: # ATTEMPT TO SEND THEM SOMEWHERE 
      trackers_list = tHandler.trackers_list
    tracker = trackers_list[int(len(trackers_list)*first_char)/256]
    redirect_cache[str(first_char)]=tracker # LOCALY CACHE THIS DECISION
    
  if scrape:
    return tracker[:-8]+ 'scrape'
    # CLEAR LOCAL CACHE
    # IT'S HERE TO AVOID UNNECESSARY WASTE OF CPU CYCLES.
    # IT GETS CHECKED, JUST NOT SO OFTEN
    if time.time()-cache_reset_time > cache_max_age:
      cache_reset_time=time.time()
      trackers_list = memcache.get('trackers_list')
      redirect_cache={} 
  else:
    return tracker
    
def redir(url):
  print 'HTTP/1.1 301 Moved Permanently\nLocation: '+url+'\n\n'

class AnnounceHandler(webapp.RequestHandler):
  def get(self):
    try:
      redir(pick_tracker(self) + '?' + self.request.query_string)
    except:
      if self.request.get('info_hash') is None:
        self.response.out.write('Invalid Request: yes its working but you need to RTFM')
      else:
        self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
        import logging
        import sys
        logging.warning('trackers_list was empty - ' + str(sys.exc_info()[0]))
        raise

class ScrapeHandler(webapp.RequestHandler):
  def get(self):
    try:
      redir(pick_tracker(self, True) + '?' + self.request.query_string)
    except:
      if self.request.get('info_hash') is None:
        self.response.out.write('Invalid Request: yes its working but you need to RTFM')
      else:
        self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
        import logging
        logging.warning('trackers_list was empty')

def main():
  application = webapp.WSGIApplication([('/announce', AnnounceHandler),
                                        ('/scrape', ScrapeHandler)])
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
