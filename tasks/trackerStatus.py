#Kopimi -- No license.

import logging
import re

from google.appengine.api import urlfetch
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

def handle_result(rpc, url):
  try:
    if rpc.get_result().status_code > 400:
      try:
        trackers_list.remove(url)
      except:
        logging.debug(url + ' was not in the list')
      logging.debug(url + ' returned ' + str(rpc.get_result().status_code))
    elif rpc.get_result().status_code == 400:
      if re.match(r".*Invalid Request.*", rpc.get_result().content, re.I) is None:
        trackers_list.remove(url)
        logging.debug(url + ' returned ' + str(rpc.get_result().status_code) + ' and body:' + rpc.get_result().content)
      else:
        logging.debug(url + ' is OK with a 400!')
    else:
      logging.debug(url + ' is OK!')
  except urlfetch.DownloadError:
    try:
      trackers_list.remove(url)
    except:
      logging.debug(url + ' was not in the list') 
    logging.debug(url + ' returned an ERROR exception!')
    

def create_callback(rpc, url):
  return lambda: handle_result(rpc, url)

def main():
  global trackers_list
  trackers_list = TrackersHandler.trackers_list[:]
  
  rpcs = []
  for url in trackers_list:
    rpc = urlfetch.create_rpc(10)
    rpc.callback = create_callback(rpc, url)
    urlfetch.make_fetch_call(rpc, url)
    rpcs.append(rpc)

  for rpc in rpcs:
    rpc.wait()

  memcache.set('trackers_list', trackers_list)

if __name__ == '__main__':
  main()