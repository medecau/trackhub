#Kopimi -- No license.

import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

class RootHandler(webapp.RequestHandler):
  
  def get(self):
    trackers_list = memcache.get('trackers_list')
    if trackers_list is None:
      trackers_list = TrackersHandler.trackers_list
      
    self.response.out.write('<html><head><title>Bittorrent tracker hub - trackhub</title><head><body>' +
                            '<center><h1>trackhub</h1><i>beta</i>' +
                            '<h2>https://trackhub.appspot.com/announce</h2><br />' +
                            '<h2>Usage:</h2>Add ' +
                            '<strong>https://trackhub.appspot.com/announce</strong>' +
                            ' has a tracker to any .torrent file.<br />' +
                            'trackhub will then redirect requests to an open tracker.<br />' +
                            'Note that the use of <i>https</i> instead of <i>http</i> is optional but advised.<br /><br />' +
                            '<h2>Trackers in the list:</h2>')
    for each_tracker in trackers_list:
      self.response.out.write(each_tracker + 'announce<br />')
    self.response.out.write('<hr /><i>Ask not what bittorrent can do for you but what can you do for bittorrent.</i><br />' +
                            '<a href="http://medecau.github.com/trackhub">kopimi</a> - ' +
                            '<a href="http://appspot.com">thanks!</a></center></body></html>')


def main():
  application = webapp.WSGIApplication([('/', RootHandler)],
                                       debug = True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
