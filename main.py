#Kopimi -- No license.

import wsgiref.handlers


from google.appengine.ext import webapp
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

tHandler = TrackersHandler()

class AnnounceHandler(webapp.RequestHandler):
  def get(self):
    self.redirect(tHandler.pick_tracker(self) + 'announce?' + self.request.query_string)

class ScrapeHandler(webapp.RequestHandler):
  def get(self):
    self.redirect(tHandler.pick_tracker(self) + 'scrape?' + self.request.query_string)


def main():
  application = webapp.WSGIApplication([('/announce', AnnounceHandler),
                                        ('/scrape', ScrapeHandler)],
                                       debug = True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
