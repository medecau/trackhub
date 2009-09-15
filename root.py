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
      
    self.response.out.write(
    '''<html><head><title>Bittorrent tracker hub - trackhub</title><head><body>
    <center><script type="text/javascript"><!--
    google_ad_client = "pub-7815980884280087";
    /* 468x15, created 9/14/09 */
    google_ad_slot = "9061282232";
    google_ad_width = 468;
    google_ad_height = 15;
    //-->
    </script>
    <script type="text/javascript"
    src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
    </script>
<h1>trackhub</h1><i>beta<small> - looking for a patron to help run the service.</small></i>
<h2>https://trackhub.appspot.com/announce</h2><br />
<h2>Usage:</h2>Add <strong>https://trackhub.appspot.com/announce</strong> has a tracker to any .torrent file.<br />
trackhub will then redirect requests to an open tracker.<br />
<small>Note that the use of <i>https</i> instead of <i>http</i> is optional but advised.<br />
Please do not use trackhub has your main tracker, think of trackhub has a spare tire for trackers.</small><br /><br />
<h2>Tracker admins:</h2>
To get included a tracker must accept connections on port 80 or 443<br />
and must accept announce requests on */announce path and scrapes on */scrape.
<h2>Trackers in the list:</h2>''')
    for each_tracker in TrackersHandler.trackers_list:
      if each_tracker in trackers_list:
        self.response.out.write('active - ')
      else:
        self.response.out.write('down - ')
      self.response.out.write(each_tracker + '<br />')
    self.response.out.write(
    '''<br /><br /><small>active: passed the test and peers are being sent.<br />
down: either did not answer in 10s,<br />
returned HTTP status code >= 400 or<br />
redirects to an unaccessible port.<br />
no peers are being sent to these trackers.</small>
<hr /><i>Ask not what bittorrent can do for you but what can you do for bittorrent.</i><br />
<a href="http://medecau.github.com/trackhub">kopimi</a> - <a href="http://appspot.com">thanks!</a></center></body></html>''')


def main():
  application = webapp.WSGIApplication([('/', RootHandler)],
                                       debug = True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
