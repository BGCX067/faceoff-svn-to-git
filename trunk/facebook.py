import os.path
import urllib2
import urllib
import simplejson
import sys

try:
    import cookielib
except ImportError:
    # If importing cookielib fails
    # let's try ClientCookie
    try:
        import ClientCookie
    except ImportError:
        # ClientCookie isn't available either
        urlopen = urllib2.urlopen
        Request = urllib2.Request
    else:
        # imported ClientCookie
        urlopen = ClientCookie.urlopen
        Request = ClientCookie.Request
        cj = ClientCookie.LWPCookieJar()

else:
    # importing cookielib worked
    urlopen = urllib2.urlopen
    Request = urllib2.Request
    cj = cookielib.LWPCookieJar()
    # This is a subclass of FileCookieJar
    # that has useful load and save methods

############################ global area
APP_ID = '' # <= I . Your facebook application id
APP_SECRET = '' # <= II. Your facebook application secret
ENDPOINT = 'graph.facebook.com'
REDIRECT_URI = 'http://127.0.0.1:8080/'
ACCESS_TOKEN = None
LOCAL_FILE = '.fb_access_token' # <= This file should be avilable where you are executing this script
STATUS_TEMPLATE = u"{name}\033[0m: {message}"

def get_url(path, args=None):
    args = args or {}
    if ACCESS_TOKEN:
        args['access_token'] = ACCESS_TOKEN
    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://"+ENDPOINT
    else:
        endpoint = "http://"+ENDPOINT
    return endpoint+path+'?'+urllib.urlencode(args)

def get(path, args=None):
    return urllib2.urlopen(get_url(path, args=args)).read()


###### grab the ACCESS_TOKEN to be used by 'get' function and grab the ID
ACCESS_TOKEN = open(LOCAL_FILE).read()
arg = sys.argv[1:][0]
dict = simplejson.loads(get('/search',args = {'q':arg, 'type':'user'}))
try:
  id = dict['data'][0]['id']
except IndexError:
  print "Congrats! Your face is not on facebook "
######
url = "https://login.facebook.com/login.php?m&next=http%3A%2F%2Fm.facebook.com%2Fprofile.php?"
id = "id=%s" % (id)
theurl = url+id
# an example url that sets a cookie,
# try different urls here and see the cookie collection you can make !

txdata = {'email':'', # <= III. The email which you want to use with this script. This script will login into this account
          'pass':'', # <= IV. Corresponding email password
	  'login':'Log In',
	 }
txdata = urllib.urlencode(txdata)	 
# if we were making a POST type request,
# we could encode a dictionary of values here,
# using urllib.urlencode(somedict)

txheaders =  {'Referer' : 'http://www.facebook.com/','User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6"'}
# fake a user agent, some websites (like google) don't like automated exploration

try:
    req = Request(theurl, txdata, txheaders)
    # create a request object

    handle = urlopen(req)
    # and open it to return a handle on the url

except IOError, e:
    print 'We failed to open "%s".' % theurl
    if hasattr(e, 'code'):
        print 'We failed with error code - %s.' % e.code
    elif hasattr(e, 'reason'):
        print "The error object has the following 'reason' attribute :"
        print e.reason
        print "This usually means the server doesn't exist,"
        print "is down, or we don't have an internet connection."
    sys.exit()

else:
    #print 'Here are the headers of the page :'
    #print handle.info()
    print handle.read() #returns the page
    #print handle.geturl() #returns the true url of the page fetched
    # (in case urlopen has followed any redirects, which it sometimes does)


