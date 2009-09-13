#Kopimi -- No license.

import wsgiref.handlers
import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

tHandler = TrackersHandler()

class AnnounceHandler(webapp.RequestHandler):
  def get(self):
    if self.request.get('info_hash') is None:
      self.redirect('/')
    try:
      self.redirect(tHandler.pick_tracker(self) + 'announce?' + self.request.query_string)
    except:
      self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
      logging.warning('trackers_list was empty')

class ScrapeHandler(webapp.RequestHandler):
  def get(self):
    if self.request.get('info_hash') is None:
      self.redirect('/')
    try:
      self.redirect(tHandler.pick_tracker(self) + 'scrape?' + self.request.query_string)
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