#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import req_proxy
import ast
from bs4 import BeautifulSoup, UnicodeDammit
#from BeautifulSoup import BeautifulSoup 
import re
import sys
from lxml import html
import HTMLParser
from Queue import Queue
from threading import Thread
import logging
import time
import threading

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 50
enclosure_queue = Queue()




def main(line, f3):
#def main(line):
    line = line.strip()
    line = ast.literal_eval(line)

    menu = line[0]
    ctlink = line[1]
    cttitle = line[2]

    if cttitle == "Home & Decor":
        cttitle = unicode(r("Home &amp; Décor"), 'utf8')
    

    #ctlink = "http://www.amazon.in/Sling-Bags/b/ref=sd_allcat_hbc_sling?ie=UTF8&node=1983351031"
    #cttitle =  "Sling & Cross-Body Bags"

    page = req_proxy.main(ctlink)
   
    soup = BeautifulSoup(page)

    tag_depatrmen = soup.find("h2", text=re.compile("Department"))
    tag_ul = tag_depatrmen.find_next("ul")

    tag_strong = tag_ul.find("strong", text = re.compile(cttitle))

    #tag_li = tag_strong.find_next("li")
    parent_li = tag_strong.find_parent("li")

    tag_narrow = None

    try:
        parent_li = parent_li.find_next_sibling()
        tag_narrow = parent_li.find("span", attrs={"class":"narrowValue"})

    except:
        print >>f3,  [menu, ctlink, cttitle, ctlink, cttitle]

         
    loop = True

    while loop is True:
	if tag_narrow is not None:
	    tag_narrow = tag_narrow.find_next("a")
            sctlink = "%s%s" %("http://www.amazon.in", tag_narrow.get("href"))
            scttitle = tag_narrow.get_text().encode("ascii", "ignore").strip()
            if scttitle != "What's this?":
                print >>f3, [menu, ctlink, cttitle, sctlink, scttitle]
            tag_narrow = tag_narrow.find("span", attrs={"class":"narrowValue"})

        else:
	    loop = False
	    



def part_threading2(i, q):
    for  line, f3 in iter(q.get, None):
        try:
            main(line, f3)

        except:
            f2 = open("page2_first_amazon_error.txt", "a+")
            print >>f2, line
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()




def mainthreading():
    f = open("to_extract_amazon.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_mn_ctl_cat.txt")
    filename2 = "%s/%s" %(directory, "f_mn_ctl_cat_scl_sct.txt")
   
    f = open(filename)
    f2 = open(filename2, "a+")

    procs = []

    for i in range(num_fetch_threads):
        #procs.append(multiprocessing.Process(target=part_threading2, args=(i, enclosure_queue,)))
        procs.append(Thread(target=part_threading2, args=(i, enclosure_queue,)))
        procs[-1].start()

    for  line  in f:
        enclosure_queue.put((line, f2))
    
    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    #for p in procs:
    #    p.join()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug('joining %s', t.getName())
        t.join()

    print "Finished everything...."
    print "closing file...."

    f.close()
    f2.close()

    #map(functools.partial(main2, soup=soup2, f = f), catlist)


def supermain():
    mainthreading()   
                   

if __name__=="__main__":
    line = "['Beauty & Health', 'http://www.amazon.in/Bath-Shower/b/ref=sd_allcat_beauty_bath/276-6718833-1247838?ie=UTF8&node=1374276031', 'Bath & Shower']"

    #line = "['Home & Kitchen', 'http://www.amazon.in/Home-D%C3%83%C2%A9cor/b/ref=sd_allcat_home_decor?ie=UTF8&node=1380374031', 'Home & Decor']"
    line = "['Home & Kitchen', 'http://www.amazon.in/Home-D%C3%83%C2%A9cor/b/ref=sd_allcat_home_decor?ie=UTF8&node=1380374031', 'Home & Decor']"
    #main(line)
    mainthreading() 
