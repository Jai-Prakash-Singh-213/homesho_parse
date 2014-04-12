import feed_proxy
from threading import Thread
from Queue import Queue
import multiprocessing
import time
import logging 

num_fetch_threads = 50
enclosure_queue = multiprocessing.JoinableQueue()

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

cl_ct_ml_mt = []



def mystrip(x):
    str(x).strip().replace("\n", " ").replace("\t", " ").replace(",", " ").replace("\r", " ")



def rss_extraction2(link):
    d = feed_proxy.main(link)

    cl = link
    ct = filter(None, link.split("/"))[-1]
    start  = ct.find("-")
    ct = ct[start +1 : ] 

    for post in d.entries:
        mt = post.title  
        start  = mt.find(")")
        mt = mt[:start+1]
        ml = post.link 

        cl_ct_ml_mt.append(map(mystrip, [ cl, ct, ml, mt]))
        print [ cl, ct, ml, mt]
         
        


def rss_brwn(i, q):
    for link  in iter(q.get, None):
        try:
            rss_extraction2(link)
            logging.debug(link)
        except:
            pass
        time.sleep(2)
        q.task_done()

    q.task_done()



def rss_extraction():
    rss_link = ["http://feeds.feedburner.com/Cat-HindiMovies",
                "http://feeds.feedburner.com/Cat-DubbedMovies", 
		"http://feeds.feedburner.com/Cat-HollywoodMovies", 
		"http://feeds.feedburner.com/Cat-TeluguMovies", 
		"http://feeds.feedburner.com/Cat-TamilMovies", 
		"http://feeds.feedburner.com/Cat-GujaratiMovies", 
		"http://feeds.feedburner.com/Cat-MalayalamMovies", 
		"http://feeds.feedburner.com/Cat-KannadaMovies", 
		"http://feeds.feedburner.com/Cat-PubjabiMovies", 
		"http://feeds.feedburner.com/Cat-BengaliMovies", 
		"http://feeds.feedburner.com/Cat-Documentary", 
                "http://feeds.feedburner.com/Cat-ShortFilms", 
		"http://feeds.feedburner.com/Cat-AdultMovies", 
		"http://feeds.feedburner.com/Cat-AnimationFilms"]

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=rss_brwn, args=(i, enclosure_queue,)))
        #procs.append(Thread(target=main3, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for link  in rss_link:
        enclosure_queue.put(link)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join(2)



def supermain():
    rss_extraction()



if __name__=="__main__":
    rss_extraction()         

    
