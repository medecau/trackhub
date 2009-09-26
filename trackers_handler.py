#Kopimi -- No license.

from google.appengine.api import memcache

class TrackersHandler():
  trackers_list = ['http://tracker.openbittorrent.com/announce',
                   'http://tracker.publicbt.com/announce',
                   'http://nemesis.1337x.org/announce',
                   'http://tracker.bittorrent.am/announce',
                   'http://tracker.publicbits.com/announce',
                   'http://tracko.appspot.com/announce',
                   'https://bittrk.appspot.com/announce']