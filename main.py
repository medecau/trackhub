#Kopimi -- No license.

import wsgiref.handlers
import sys
import time
import re
import urllib
from google.appengine.ext import webapp
from google.appengine.api import memcache
from trackers_handler import TrackersHandler


## LOCAL CACHING

tHandler = TrackersHandler()
cache_max_age=300
trackers_list = memcache.get('trackers_list')
cache_reset_time=0
redirect_cache={}


def pick_tracker (self, scrape=False): #CHOOSE ONE TRACKER
  global tHandler, cache_max_age, trackers_list, cache_reset_time, redirect_cache
  
  if time.time()-cache_reset_time > cache_max_age: # CLEAR LOCAL CACHE
    cache_reset_time=time.time()
    trackers_list = memcache.get('trackers_list')
    redirect_cache={}
    
  # GET THE INT VALUE OF THE FIRST BYTE FROM THE HASH INFO 
  urlencoded_info_hash=re.match(r".*info_hash=([^?]+).*", self.request.query_string).group(1)
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
  else:
    return tracker

class AnnounceHandler(webapp.RequestHandler):
  def get(self):
    try:
      #self.response.headers.add_header("Expires", time.asctime( time.gmtime(time.time()+86400)) + " GMT")
      #self.response.headers.add_header("Cache-Control", "max-age = 86400")
      self.redirect(pick_tracker(self) + '?' + self.request.query_string, permanent=True)
    except:
      if self.request.get('info_hash') is None:
        self.response.out.write('Invalid Request: yes its working but you need to RTFM')
      else:
        self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
        import logging
        logging.warning('trackers_list was empty - ' + str(sys.exc_info()[0]))
        raise

class ScrapeHandler(webapp.RequestHandler):
  def get(self):
    if self.request.get('info_hash') is None:
      self.response.out.write('Invalid Request: yes its working but you need to RTFM')
    try:
      self.redirect(pick_tracker(self, True) + '?' + self.request.query_string, permanent=True)
    except:
      self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
      import logging
      logging.warning('trackers_list was empty')

def profile_main():
  # This is the main function for profiling 
  # We've renamed our original main() above to real_main()
  import cProfile, pstats, StringIO, logging
  prof = cProfile.Profile()
  prof = prof.runctx("real_main()", globals(), locals())
  stream = StringIO.StringIO()
  stats = pstats.Stats(prof, stream=stream)
  stats.sort_stats("time")  # Or cumulative
  stats.print_stats(80)  # 80 = how many to print
  # The rest is optional.
  # stats.print_callees()
  # stats.print_callers()
  logging.info("Profile data:\n%s", stream.getvalue())

def real_main():
  application = webapp.WSGIApplication([('/announce', AnnounceHandler),
                                        ('/scrape', ScrapeHandler)],
                                       debug = True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  #main=real_main
  main=profile_main
