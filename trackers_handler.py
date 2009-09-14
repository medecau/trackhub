#Kopimi -- No license.

import urllib
import re

from google.appengine.api import memcache

class TrackersHandler():
  trackers_list = ['http://tracker.openbittorrent.com/announce',
                   'http://tracker.publicbt.com/announce',
                   'http://nemesis.1337x.org/announce',
                   'http://tracker.bittorrent.am/announce',
                   'http://tracker.publicbits.com/announce',
                   'http://tracko.appspot.com/announce',
                   'https://bittrk.appspot.com/announce']
  def pick_tracker (self, rself, scrape=False):
    trackers_list = memcache.get('trackers_list')
    if trackers_list is None:
      trackers_list = self.trackers_list

    first_char = re.match(r".*info_hash=(.).*", urllib.unquote(rself.request.query_string))
    first_char_int = ord(first_char.group(1))
    tracker = trackers_list[int(len(trackers_list)*first_char_int)/256]
    if scrape:
      return tracker.replace('announce', 'scrape')
    else:
      return tracker