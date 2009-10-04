#Kopimi -- No license.

from google.appengine.api import memcache

class TrackersHandler():
  trackers_list = ['http://bittrk.appspot.com/announce',
                   'http://nemesis.1337x.org/announce',
                   'http://torrent.ipnm.ru/announce',
                   'http://tracker.bittorrent.am/announce',
                   'http://tracker.openbittorrent.com/announce',
                   'http://tracker.publicbt.com/announce',
                   'https://bittrk.appspot.com/announce',
                   'https://memtracker.appspot.com/announce'].sort()