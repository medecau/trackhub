#Kopimi -- No license.

from google.appengine.api.memcache import get
from google.appengine.api.memcache import set
from os import environ
from re import compile
from re import match
from trackers_handler import TrackersHandler
from urllib import unquote

## LOCAL CACHING

tHandler = TrackersHandler()
trackers_list = get('trackers_list')
info_hash_pattern=compile(r".*info_hash=([^?]+).*")


def main():
  global trackers_list
  
  # GET THE INT VALUE OF THE FIRST BYTE FROM THE HASH INFO 
  urlencoded_info_hash=info_hash_pattern.match(environ['QUERY_STRING']).group(1)
  first_char = ord(unquote(urlencoded_info_hash)[:1])
  
  if trackers_list is None: # ATTEMPT TO SEND THEM SOMEWHERE 
    trackers_list = tHandler.trackers_list[:]
  tracker = trackers_list[first_char%len(trackers_list)]

  if environ['PATH_INFO'][1:2] == 'a': # FOR ANNOUNCES
    print 'Status: 301 Moved Permanently\nLocation: '+tracker+'?'+environ['QUERY_STRING']+'\n'
    
  elif environ['PATH_INFO'][1:2] == 's': # FOR SCRAPES
    print 'Status: 301 Moved Permanently\nLocation: '+tracker[:-8]+'scrape?'+environ['QUERY_STRING']+'\n'

if __name__ == '__main__':
  main()