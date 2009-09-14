#Kopimi -- No license.

import wsgiref.handlers
import logging
import sys

from google.appengine.ext import webapp
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

tHandler = TrackersHandler()

class AnnounceHandler(webapp.RequestHandler):
  def get(self):
    if self.request.get('info_hash') is None:
      self.response.out.write('Invalid Request: yes its working but you need to RTFM')
    try:
      #self.redirect(tracker=tHandler.pick_tracker(self) + '?redir=trackhub&' + self.request.query_string)
      tracker=tHandler.pick_tracker(self) + '?redir=trackhub&' + self.request.query_string
      print 'HTTP Status Code: HTTP/1.1 301 Moved Permanently '
      print 'Location: ' + tracker
      print ''
    except:
      self.response.out.write('d14:failure reason31:No trackers available, sorry :(e')
      logging.warning('trackers_list was empty')

class ScrapeHandler(webapp.RequestHandler):
  def get(self):
    if self.request.get('info_hash') is None:
      self.response.out.write('Invalid Request: yes its working but you need to RTFM')
    try:
      self.redirect(tHandler.pick_tracker(self, True) + '?' + self.request.query_string)
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
