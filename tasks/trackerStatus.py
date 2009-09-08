from google.appengine.api import urlfetch
from google.appengine.api import memcache

def handle_result(rpc, url):
  try:
    if rpc.get_result().status_code >= 400:
      trackers_list.remove(url)
  except urlfetch.DownloadError:
    trackers_list.remove(url)

def create_callback(rpc, url):
  return lambda: handle_result(rpc, url)

trackers_list = ['http://tracker.openbittorrent.com/',
                 'http://tracker.publicbt.com/',
                 'http://nemesis.1337x.org/',
                 'http://tracker.bittorrent.am/',
                 'http://tracker.publicbits.com/',
                 'http://tracko.appspot.com/']

rpcs = []
for url in trackers_list:
  rpc = urlfetch.create_rpc(10)
  rpc.callback = create_callback(rpc, url)
  urlfetch.make_fetch_call(rpc, url)
  rpcs.append(rpc)

for rpc in rpcs:
  rpc.wait()

memcache.set('trackers_list', trackers_list)