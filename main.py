#Kopimi -- No license.

from re import compile, match
from os import environ
from google.appengine.api.memcache import get, set
from trackers_handler import TrackersHandler
from time import time
from urllib import unquote

## LOCAL CACHING

tHandler = TrackersHandler()
trackers_list = get('trackers_list')
cache_reset_time=0
cache_sync_time=0
redirect_cache={}
info_hash_pattern=compile(r".*info_hash=([^?]+).*")


def main():
  global tHandler, trackers_list, cache_reset_time, redirect_cache
  
  # GET THE INT VALUE OF THE FIRST BYTE FROM THE HASH INFO 
  urlencoded_info_hash=info_hash_pattern.match(environ['QUERY_STRING']).group(1)
  first_char = ord(unquote(urlencoded_info_hash)[:1])
  
  if trackers_list is None: # ATTEMPT TO SEND THEM SOMEWHERE 
    trackers_list = tHandler.trackers_list
  tracker = trackers_list[int(len(trackers_list)*first_char)/256]

  
  if environ['PATH_INFO'][1:2] == 'a': # FOR ANNOUNCES
    print 'Status: 301 Moved Permanently\nLocation: '+tracker+'?'+environ['QUERY_STRING']+'\n'
    
  elif environ['PATH_INFO'][1:2] == 's': # FOR SCRAPES
    print 'Status: 301 Moved Permanently\nLocation: '+tracker[:-8]+'scrape?'+environ['QUERY_STRING']+'\n'

if __name__ == '__main__':
  main()