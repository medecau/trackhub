#Kopimi -- No license.

import wsgiref.handlers
import logging
import sys
import time
import re
from google.appengine.ext import webapp
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

tHandler = TrackersHandler()
ih_1stbyte_pattern = re.pattern(r".*info_hash=(.).*")
local_cache_timer=time.time()


def pick_tracker (self, rself, scrape=False):
  trackers_list = memcache.get('trackers_list')
  if trackers_list is None:
    trackers_list = tHandler.trackers_list

  first_char = re.match(ih_1stbyte_patterny, urllib.unquote(rself.request.query_string))
  first_char_int = ord(first_char.group(1))
  tracker = trackers_list[int(len(trackers_list)*first_char_int)/256]
  if scrape:
    return tracker.replace('announce', 'scrape')
  else:
    return tracker

class AnnounceHandler(webapp.RequestHandler):
  def get(self):
    try:
      self.response.headers.add_header("Expires", time.asctime( time.gmtime(time.time()+86400)) + " GMT")
      self.response.headers.add_header("Cache-Control", "max-age = 86400")
      self.redirect(pick_tracker(self) + '?' + self.request.query_string, permanent=True)
    except:
      if self.request.get('info_hash') is None:
        self.response.out.write('Invalid Request: yes its working but you need to RTFM')
      else:
        self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
        logging.warning('trackers_list was empty - ' + str(sys.exc_info()[0]))

class ScrapeHandler(webapp.RequestHandler):
  def get(self):
    if self.request.get('info_hash') is None:
      self.response.out.write('Invalid Request: yes its working but you need to RTFM')
    try:
      self.redirect(pick_tracker(self, True) + '?' + self.request.query_string, permanent=True)
    except:
      self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
      logging.warning('trackers_list was empty')

def profile_main():
  # This is the main function for profiling 
  # We've renamed our original main() above to real_main()
  import cProfile, pstats, StringIO
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
  main=profile_main
