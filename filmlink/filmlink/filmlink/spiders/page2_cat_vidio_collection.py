# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

import req_proxy
from bs4 import BeautifulSoup
import multiprocessing
import logging
import time
import os
import re 
from lxml import html

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 300
enclosure_queue = multiprocessing.JoinableQueue()




def  main2(line):
    f = open("to_extract_cat.txt")
    directory = f.read().strip()
    f.close()

    filename2 = "%s/%s" %(directory, "f_ct_cl_st_sl_vt_wp_wl_img.txt")
    
    f2 = open(filename2, "a+")
 
    line2 = line.split(",")
    catlink = str(line2[0]).strip()
    cattitle = str(line2[1]).replace("\n", " ").replace("\t", "").replace("\r", "").strip()
    
    sub_catlink = line2[2]
    sub_cattitle = line2[3].replace("\n", " ").replace("\t", "").replace("\r", "").strip()

    end = sub_cattitle.find(")").strip()
    
    if end != -1:
        sub_cattitle = sub_cattitle[:end+1]
    
    page = req_proxy.main(sub_catlink)   
    
    soup = BeautifulSoup(page)
    tree = html.fromstring(page)
    
    image = "None"

    if tree is not None:
        image = str(tree.xpath('/html/body/div/div/div[5]/div/div[2]/div/div/div[3]/a/img/@src')[0]).strip()


    tag_hotserver  = soup.find_all("span", text=re.compile("Host Server"))

    for l in tag_hotserver:
        loop  = True
        video_type =  str(l.next_sibling).replace("\n", " ").replace("\t", "").replace("\r", "").strip()
        next_a = l.find_next("a")

	while loop is True:
            try:
	        tag_nm = str(next_a.name).strip()

	        if tag_nm == "br":
	            pass

	        if tag_nm == "a":
	            watchlink = str(next_a.get("href")).strip()
                    watchpart = str(next_a.get_text()).replace("\n", " ").replace("\t", "").replace("\r", "").strip()
                    print >>f2,  ','.join([cattitle, catlink, sub_cattitle, sub_catlink, video_type, watchpart, watchlink, image])
                    print ','.join([cattitle, catlink, sub_cattitle, sub_catlink, video_type, watchpart, watchlink, image]) 
     
                if tag_nm != "a" and tag_nm != "br":
                    loop = False
   
                next_a = next_a.find_next_sibling()

            except:
                loop  = False
        
    f.close()



def mainthreading2(i, q):
    for line in iter(q.get, None):
        try:
            main2(line)
            print line

        except:
            f2 = open("page1_first_cat_error2.txt", "a+")
            print >>f2, line
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()


 
def main():
    f = open("to_extract_cat.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_cl_ct_sl_st.txt")

    f = open(filename)

    procs = [] 

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=mainthreading2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()   

    for line in f:
        enclosure_queue.put(line)

    f.close()

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'
    
    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()
    
    for p in procs:
        p.join()

    print "Finished everything...."
    print "num active children:", multiprocessing.active_children()

    f.close()

if __name__=="__main__":
    main()


