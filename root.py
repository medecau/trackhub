#Kopimi -- No license.

import wsgiref.handlers
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache

from trackers_handler import TrackersHandler

class RootHandler(webapp.RequestHandler):
  
  def get(self):
    cached_trackers_list = memcache.get('trackers_list')
    trackers_list=''
    for tracker in TrackersHandler.trackers_list:
      if tracker in cached_trackers_list:
        trackers_list+='<li>Active: ' + tracker + '</li>'
      else:
        trackers_list+='<li>Down: ' + tracker + '</li>'
    
    
    template_values = {
      'trackers_list': trackers_list,
      }
        
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', RootHandler)],
                                       debug = True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
