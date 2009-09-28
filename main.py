#Kopimi -- No license.
from re import compile, match
from os import environ
from google.appengine.api.memcache import get
from trackers_handler import TrackersHandler
from time import time
import urllib

## LOCAL CACHING

tHandler = TrackersHandler()
trackers_list = get('trackers_list')
cache_reset_time=0
redirect_cache={}
info_hash_pattern=compile(r".*info_hash=([^?]+).*")


def main():
  global tHandler, trackers_list, cache_reset_time, redirect_cache
  
  # GET THE INT VALUE OF THE FIRST BYTE FROM THE HASH INFO 
  urlencoded_info_hash=info_hash_pattern.match(environ['QUERY_STRING']).group(1)
  first_char = ord(urllib.unquote(urlencoded_info_hash)[:1])
  
  try: # TRY TO GET THE PICK FROM LOCAL MEMORY CACHE
    tracker=redirect_cache[str(first_char)]
  except:
    if trackers_list is None: # ATTEMPT TO SEND THEM SOMEWHERE 
      trackers_list = tHandler.trackers_list
    tracker = trackers_list[int(len(trackers_list)*first_char)/256]
    redirect_cache[str(first_char)]=tracker # LOCALY CACHE THIS DECISION
  
  if environ['PATH_INFO'][1:2] == 'a': # FOR ANNOUNCES
    print 'Status: 301 Moved Permanently\nLocation: '+tracker+'?'+environ['QUERY_STRING']+'\n'
    
  elif environ['PATH_INFO'][1:2] == 's': # FOR SCRAPES
    print 'Status: 301 Moved Permanently\nLocation: '+tracker[:-8]+'scrape'+'?'+environ['QUERY_STRING']+'\n'
    
    # CLEAR LOCAL CACHE
    # IT GET'S CHECKED, JUST NOT SO OFTEN
    if time()-cache_reset_time > 300:
      cache_reset_time=time()
      new_trackers_list = get('trackers_list')
      if trackers_list != new_trackers_list: # IF THE LIST CHANGED IT MAY NEED TO GET UPDATED
        try:
          if len(trackers_list) >= len(new_trackers_list): # LET'S ASSUME THE LIST ONLY NEEDS TO GET UPDATED WHEN ITS EITHER THE SAME SIZE OR SMALLER
            redirect_cache={}
        except:
          redirect_cache={}
        trackers_list = new_trackers_list

if __name__ == '__main__':
  main()