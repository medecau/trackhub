import urllib
import re

from google.appengine.api import memcache

class TrackersHandler():
  trackers_list = ['http://tracker.openbittorrent.com/',
                   'http://tracker.publicbt.com/',
                   'http://nemesis.1337x.org/',
                   'http://tracker.bittorrent.am/',
                   'http://tracker.publicbits.com/',
                   'http://tracko.appspot.com/']
  def pick_tracker (self, rself):
    trackers_list = memcache.get('trackers_list')
    if trackers_list is None:
      trackers_list = self.trackers_list

    first_char = re.match(r".*info_hash=(.).*", urllib.unquote(rself.request.query_string))
    first_char_int = ord(first_char.group(1))
    return trackers_list[int(float(len(trackers_list))/256*first_char_int)]