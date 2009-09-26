from google.appengine.api import memcache

def main():
  memcache.flush_all()
  print ''
  print 'done'

if __name__ == "__main__":
  main()