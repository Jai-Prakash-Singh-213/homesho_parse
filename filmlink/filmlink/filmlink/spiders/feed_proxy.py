import urllib2, feedparser
from random import choice
import logging
import socket


socket.setdefaulttimeout(10)
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')




def main(link):
    f = open("/home/desktop/proxy_http_auth.txt")
    #f = open("/home/user/Desktop/proxy5")
    #f = open("/home/user/Desktop/proxy_http_auth.txt")
    pass_ip_list = f.read().strip().split("\n")
    f.close()
  
    header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0'}

    for l in xrange(6):
        pass_ip = choice(pass_ip_list)
        pass_ip = pass_ip.strip()
        #pass_ip = "vinku:india123@%s" %(pass_ip.strip())

        try:
            http_proxy = "http://" + pass_ip
            proxyDict = {"http"  :http_proxy}
           
            proxy = urllib2.ProxyHandler(proxyDict)
            d = feedparser.parse(link, handlers = [proxy], agent = header)    
            return d
        except:
            pass

    return None




if __name__=="__main__":
    link = "http://feeds.feedburner.com/Cat-HindiMovies"
    d = main(link)
    
    for post in d.entries:
          print post.title + ": " + post.link + "\n"

