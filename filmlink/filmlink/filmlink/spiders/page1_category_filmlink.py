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

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 50 
enclosure_queue = multiprocessing.JoinableQueue()




def main2(line, filename):
    catlink = line[0]
    cattitle = line[1]

    f = open(filename, "a+")

    page = req_proxy.main(catlink)

    soup = BeautifulSoup(page)

    tag_page = soup.find("div", attrs={"id":"wp_page_numbers"})

    tag_page_a_list = []

    if tag_page:
        tag_page_a = tag_page.find_all("a")[:-1]

	for cat_page in tag_page_a:
	    sub_page_link = str(cat_page.get("href")).strip()

	    sub_page =  req_proxy.main(sub_page_link)

	    sub_soup = BeautifulSoup(sub_page)

            tag_content_a  = soup.find_all("h2", attrs={"class":"title"})

	    for subcatlinktitle in tag_content_a:
	        subcatlink = str(subcatlinktitle.a.get("href")).strip()
		subcattitle = subcatlinktitle.get_text().encode("ascii", "ignore")
                subcattitle = str(subcattitle).strip().replace("\n", "").replace("\t", "").replace(",", "")
		print >>f, ",".join([catlink, cattitle, subcatlink, subcattitle])

    else:
	tag_content_a  = soup.find_all("h2", attrs={"class":"title"})

	for subcatlinktitle in tag_content_a:
	    subcatlink = str(subcatlinktitle.a.get("href")).strip()
	    subcattitle = subcatlinktitle.get_text().encode("ascii", "ignore")
            subcattitle = str(subcattitle).strip().replace("\n", "").replace("\t", "").replace(",", "")
            print >>f,  ",".join([catlink, cattitle, subcatlink, subcattitle])
    
    f.close()



	    
def mainthreading2(i, q):
    for ml_mt_sub , filename in iter(q.get, None):
        try:
            main2(ml_mt_sub, filename)
            #print ml_mt_sub

        except:
            f2 = open("page1_first_cat_error.txt", "a+")
            print >>f2, ml_mt_sub
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()




def mainthreading(catlink_cattitle):
    f = open("to_extract_cat.txt", "a+")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_cl_ct_sl_st.txt")

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=mainthreading2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for  ml_mt_sub in catlink_cattitle:
        enclosure_queue.put((ml_mt_sub, filename))

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




def main():
    directory = "dir%s/categories" %(time.strftime("%d%m%Y"))

    try:
        os.makedirs(directory)

    except:
        pass

    f = open("to_extract_cat.txt", "w+")
    print >>f, directory
    f.close()

    f = open("extracted_cat.txt", "a+")
    print >>f, directory
    f.close()

    link = "http://www.filmlinks4u.net/"

    page = req_proxy.main(link)

    soup = BeautifulSoup(page)
    
    tag_cat = soup.find("li", attrs={"id":"categories-3"})

    tag_cat_a_list = tag_cat.find_all("a")

    catlink_cattitle = []

    for al in tag_cat_a_list:
        catlink = str(al.get("href")).strip()
        cattitle = str(catlink.split("/")[-1]).strip().replace(",", "").replace("\n", "").replace("\t", "")
    
        catlink_cattitle.append([catlink, cattitle])

    mainthreading(catlink_cattitle)




if __name__=="__main__":
    main()

