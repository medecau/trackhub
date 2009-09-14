#Kopimi -- No license.

import urllib
import re

from google.appengine.api import memcache

class TrackersHandler():
  trackers_list = ['http://tracker.openbittorrent.com/announce',
                   'http://tracker.publicbt.com/announce',
                   'http://nemesis.1337x.org/announce',
                   'http://tracker.bittorrent.am/announce',
                   'http://tracker.publicbits.com/announce'
                   'http://tracko.appspot.com/announce',
                   'https://bittrk.appspot.com/announce']
  def pick_tracker (self, rself, scrape=False):
    trackers_list = memcache.get('trackers_list')
    if trackers_list is None:
      trackers_list = self.trackers_list

    first_char = re.match(r".*info_hash=(.).*", urllib.unquote(rself.request.query_string))
    if first_char is None:
      first_char_int = 0
    else:
      first_char_int = ord(first_char.group(1))
    tracker = trackers_list[int(float(len(trackers_list))/256*first_char_int)]
    if scrape:
      tracker = tracker.replace('announce', 'scrape')
    return tracker