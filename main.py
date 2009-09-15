#Kopimi -- No license.

import wsgiref.handlers
import logging
import sys
import time

from google.appengine.ext import webapp
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

tHandler = TrackersHandler()

class AnnounceHandler(webapp.RequestHandler):
  def get(self):
    try:
      self.response.headers.add_header("Expires", str(time.asctime( time.gmtime(time.time()+86400))) + " GMT")
      self.redirect(tHandler.pick_tracker(self) + '?' + self.request.query_string, permanent=True)
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
      self.redirect(tHandler.pick_tracker(self, True) + '?' + self.request.query_string, permanent=True)
    except:
      self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
      logging.warning('trackers_list was empty')


def main():
  application = webapp.WSGIApplication([('/announce', AnnounceHandler),
                                        ('/scrape', ScrapeHandler)],
                                       debug = True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
