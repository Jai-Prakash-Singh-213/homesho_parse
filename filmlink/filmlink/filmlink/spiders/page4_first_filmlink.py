#!/usr/bin/env python 
from Queue import Queue
from threading import Thread
import logging
import time
import os


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

# page3_first_filedivision_jobong.py page3_second_scrapy_jobong.py

num_fetch_threads = 100
enclosure_queue = Queue()



def main4(line, directory):
    line2 = line.strip().split(",")
   
    dirtwo = "%s/%s" %(directory, line2[0].strip())

        

    try:
        os.makedirs(dirtwo)

    except:
        pass

    filename = "%s/%s" %(dirtwo, "f_ct_cl_st_sl_tp_prt_em_im_wl.csv")

    f2 = open(filename, "a+") 

    #if str(line2[5]).strip() == "Watch Online Full Movie":
    print >>f2, str(line).strip()
    print line

    f2.close()




def main3(i, q):
    for line, directory  in iter(q.get, None):

        main4(line, directory)

        logging.debug(line)

        time.sleep(i + 2)
        q.task_done()

    q.task_done()





def main():
    f = open("to_extract_cat.txt")
    directory = f.read().strip()
    f.close()

    filename =  "%s/%s" %(directory, "f_ct_cl_st_sl_tp_prt_em_im_wl.csv")

    procs = []

    

    for i in range(num_fetch_threads):
        procs.append(Thread(target=main3, args=(i, enclosure_queue,)))
	#worker.setDaemon(True)
	procs[-1].start()

    f = open(filename)
    
    for line  in f:
        enclosure_queue.put((line, directory))
        
    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)
 
    enclosure_queue.join()

    for p in procs:
        p.join()



if __name__=="__main__":

    #line = "oriya,http://www.filmlinks4u.net/category/oriya,Panjur Bhitare Sari (1992),http://www.filmlinks4u.net/2012/06/panjur-bhitare-sari-1992-oriya-movie-watch-online.html,- Youtube,Watch Online Full Movie,http://ads.videolinkz.us/300x250-2.html,http://www.filmlinks4u.net/wp-content/uploads/2012/06/Panjur-Bhitare-Sari-1992-Oriya-Movie-Watch-Online.jpg,http://nobuffer.info/yt.php?url=LF-KJQnE8lw&feature"

    #directory = "dir06032014"
    #main4(line, directory)

    main()
