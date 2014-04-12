import req_proxy
import ast
from bs4  import BeautifulSoup
import re
import sys
from Queue import Queue
from threading import Thread
import logging
import time
import threading
import multiprocessing

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 100
enclosure_queue = multiprocessing.JoinableQueue()




def mystrip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()




def main2(line, all_brand_link, f3):
    menu = line[0]
    ctlink = line[1]
    cttitle = line[2]
    sctlink = line[3]
    scttitle = line[4]

    page = req_proxy.main(all_brand_link)
    soup = BeautifulSoup(page)

    tag_brand_uls = soup.find_all("ul", attrs={"class":"column"})

    for ul_brand_link in tag_brand_uls:
        all_brand_link = ul_brand_link.find_all("a")
        for bl_bt in all_brand_link:
	    bl = "%s%s" %("http://www.amazon.in", bl_bt.get("href"))
	    bt = str(bl_bt.span.get_text()).strip()

            filedata = [menu, ctlink, cttitle, sctlink, scttitle, bl, bt]
            filedata2 = map(mystrip, filedata)
	    logging.debug(filedata2)

            f4 = open(f3, "a+")
            print >>f4, filedata2
            f4.close()


        

def main(line, f3):
   line = line.strip()
   line = ast.literal_eval(line)
    
   menu = line[0]
   ctlink = line[1]
   cttitle = line[2]
   sctlink = line[3]
   scttitle = line[4]

   page = req_proxy.main(sctlink)
   
   soup = BeautifulSoup(page)

   tag_brands = soup.find("h2", text=re.compile("Brands"))

   tag_ul = tag_brands.find_next("ul")

   tag_span_see_more = tag_ul.find("span", attrs={"class":"refinementLink seeMore"}) 

   if tag_span_see_more is not None:
       all_brand_link =  "%s%s" %("http://www.amazon.in" , tag_span_see_more.find_parent("a").get("href"))
       main2(line, all_brand_link, f3)

   else:
       tag_al = tag_ul.find_all("a")
       for al in tag_al:
           bl = "%s%s" %("http://www.amazon.in", al.get("href"))
	   bt = al.span.get_text().encode("ascii", "ignore")
           
           filedata = [menu, ctlink, cttitle, sctlink, scttitle, bl, bt]
           filedata2 = map(mystrip, filedata)

           logging.debug(filedata2)
           f4 = open(f3, "a+")
           print >>f4, filedata2
           f4.close()
           



def part_threading2(i, q):
    for  line, f3 in iter(q.get, None):
        try:
            main(line, f3)
            print line

        except:
            f2 = open("page3_first_amazon_error.txt", "a+")
            print >>f2, line
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()




def mainthreading():
    f = open("to_extract_amazon.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_mn_ctl_cat_scl_sct.txt")
    filename2 = "%s/%s" %(directory, "f_mn_ctl_cat_scl_sct_bl_bt.txt")

    f = open(filename)
    f2 = filename2

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=part_threading2, args=(i, enclosure_queue,)))
        procs[-1].start()

    for  line  in f:
        enclosure_queue.put((line, f2))

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
    supermain()
    
    
