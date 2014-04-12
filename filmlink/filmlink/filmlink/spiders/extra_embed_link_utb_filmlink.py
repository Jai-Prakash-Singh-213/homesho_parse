#!/usr/bini/env python 
import phan_proxy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from lxml import html
import logging
import multiprocessing
import time 
import sys

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 300
enclosure_queue = multiprocessing.JoinableQueue()




def main(line):
    filename2 = "dt_movie2.csv"

    f2 = open(filename2, "a+")

    line2 = line.strip().split(",")

    line2 = map(str.strip,  line2)

    cattitle = line2[1]
    catlink = line2[2]
    subcattitle = line2[3]
    subcatlink = line2[4]
    tpe = line2[5]
    prt = line2[6]
    wl = line2[-3]
    img = line2[-4]

    wl = wl.replace('"', " ").strip()
    driver = phan_proxy.main(wl)
     
    page = driver.page_source
    tree = html.fromstring(page)

    embedlink =  tree.xpath("/html/body/div[2]/center/div/div/div[2]/iframe/@src")
    embedlink2 =  tree.xpath("/html/body/object/embed/@src")
    embedlink3 =  tree.xpath("/html/body/div[2]/center/div/div/div[2]/object/embed/@src")

    if embedlink3  is not None:
        print >>f2, ','.join([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink3[0]).strip(), img,  wl])
        logging.debug([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink3[0]).strip(), img,  wl])

    elif embedlink2 is not None:
        print >>f2, ','.join([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink2[0]).strip(), img,  wl])
        logging.debug([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink2[0]).strip(), img,  wl])

    elif embedlink is  not None:
        print >>f2, ','.join([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink[0]).strip(), img,  wl])
        logging.debug([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink[0]).strip(), img,  wl])

    else:
        f3 = open("page3_filmlink_embedlink_error2.txt", "a+")
        print >>f3, line
        f3.close()

    driver.delete_all_cookies()
    driver.quit()
    f2.close()
    



def mainthreading2(i, q):
    for line in iter(q.get, None):
        try:
            main(line)
            print line

        except:
            f2 = open("page3_filmlink_embedlink_error.txt", "a+")
            print >>f2, line
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()




def mainthreading():
    filename  = "dt_movie.csv"

    f = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=mainthreading2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for line in f:
        enclosure_queue.put(line)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join(2)

    print "Finished everything...."
    print "num active children:", multiprocessing.active_children()

    f.close()



if __name__=="__main__":
    #line = """"316","nepali","http://www.filmlinks4u.net/category/nepali","Shahid Gate (2002)","http://www.filmlinks4u.net/2010/02/shahid-gate-2002-nepali-movie-watch.html","- Youtube","Watch Online Full Movie",,"http://1.bp.blogspot.com/_51uA4Ku6DYw/S4ouVcq7_JI/AAAAAAAACX4/QIVJIVz7uK8/s400/Shahid+Gate+%282002%29+-+Nepali+Movie+Watch+Online.jpg","http://video-links.info/yt.php?url=uPNujTd7mcw",,"A" """
    #main(line)
    mainthreading()
