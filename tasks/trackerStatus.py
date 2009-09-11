#Kopimi -- No license.

import logging

from google.appengine.api import urlfetch
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

def handle_result(rpc, url):
  try:
    if rpc.get_result().status_code >= 400:
      trackers_list.remove(url)
      logging.debug(url + ' returned ' + str(rpc.get_result().status_code))
    else:
      logging.debug(url + ' is OK!')
  except urlfetch.DownloadError:
    trackers_list.remove(url)
    logging.debug(url + ' returned an ERROR exception!')
    

def create_callback(rpc, url):
  return lambda: handle_result(rpc, url)

trackers_list = TrackersHandler.trackers_list

rpcs = []
for url in trackers_list:
  rpc = urlfetch.create_rpc(10)
  rpc.callback = create_callback(rpc, url)
  urlfetch.make_fetch_call(rpc, url)
  rpcs.append(rpc)

for rpc in rpcs:
  rpc.wait()

memcache.set('trackers_list', trackers_list)