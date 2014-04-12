import ast
import req_proxy
from bs4 import BeautifulSoup
import time 
import re
import sys
from Queue import Queue
from threading import Thread
import logging
import threading
import multiprocessing
import os 

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 100
enclosure_queue = multiprocessing.JoinableQueue()




def mystrip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()




def main2(line, direct, link = None):
    menu = line[0]
    catlink = line[1]
    cattitle = line[2]
    scatlink = line[3]
    scattitle = line[-3]
    bl = line[-2]
    bt = line[-1]

    page = req_proxy.main(link)
    soup = BeautifulSoup(page)

    #prlink = soup.find_all("h3", attrs={"class":"newaps"})
    prlink = soup.find_all("div", attrs={"class":"image imageContainer"})

    filedoc = "%s/%s.doc" %(direct, bt)
    filedocx = "%s/%s.docx" %(direct, bt)

    f = open(filedoc, "a+")
    f2 = open(filedocx, "a+")

    for plimg in prlink:
        pl = str(plimg.a.get("href"))
        imgl = str(plimg.a.img.get("src"))
        print >>f, [menu, catlink, cattitle, scatlink, scattitle, bl, bt, pl, imgl]
	print >>f2, pl

    f.close()
    f2.close()

    prlinknext = soup.find("a", attrs={"id":"pagnNextLink"})

    time.sleep(1)

    if prlinknext is not None:
        prlinknext = "%s%s" %("http://www.amazon.in" , prlinknext.get("href"))
        main2(line, direct, link = prlinknext)
        #print prlinknext




def main(line, directory):
    line = line.strip()
    line = ast.literal_eval(line)    
    menu = line[0]
    catlink = line[1]
    cattitle = line[2]
    scatlink = line[3]
    scattitle = line[-3]
    bt = line[-1]
    bl = line[-2]

    direct = "%s/%s/%s/%s/%s" %(directory, menu, cattitle, scattitle, bt)    

    try:
        os.makedirs(direct)
    except:
        pass

    main2(line, direct,  link = bl)




def part_threading2(i, q):
    for  line, directory in iter(q.get, None):
        try:
            main(line, directory)

        except:
            f2 = open("page4_first_amazon_error.txt", "a+")
            print >>f2, line
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()




def mainthreading():
    f = open("to_extract_amazon.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_mn_ctl_cat_scl_sct_bl_bt.txt")

    f = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=part_threading2, args=(i, enclosure_queue,)))
        procs[-1].start()

    for  line  in f:
        enclosure_queue.put((line, directory))

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()

    #main_thread = threading.currentThread()

    #for t in threading.enumerate():
    #    if t is main_thread:
    #        continue
    #    logging.debug('joining %s', t.getName())
    #    t.join(2)

    print "Finished everything...."
    print "closing file...."

    f.close()




def supermain():
    mainthreading()




if __name__=="__main__":
    line = "['Home & Kitchen', 'http://www.amazon.in/Bedroom-Linen/b/ref=sd_allcat_bedroom_linen?ie=UTF8&node=1380447031', 'Bedroom Linen', 'http://www.amazon.in/s/ref=lp_1380447031_nr_n_2/275-5451017-1825336?rh=n%3A976442031%2Cn%3A%21976443031%2Cn%3A1380442031%2Cn%3A1380447031%2Cn%3A1380449031&bbn=1380447031&ie=UTF8&qid=1394881750&rnid=1380447031', 'Bedspreads(823)', 'http://www.amazon.in/s/ref=sr_in_-2_p_89_17/275-5451017-1825336?rh=n%3A976442031%2Cn%3A%21976443031%2Cn%3A1380442031%2Cn%3A1380447031%2Cn%3A1380449031%2Cp_89%3AGreenland&bbn=1380449031&ie=UTF8&qid=1395067308&rnid=3837712031', 'Greenland']"

    #main(line)

    supermain()
