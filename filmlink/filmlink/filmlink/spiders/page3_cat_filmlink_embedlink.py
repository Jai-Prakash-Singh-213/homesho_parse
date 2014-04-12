#!/usr/bini/env python 
import phan_proxy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from lxml import html
import logging
import multiprocessing
import time 

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 300
enclosure_queue = multiprocessing.JoinableQueue()

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)




def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass




def main(line):
    f = open("to_extract_cat.txt")
    directory = f.read().strip()
    f.close()

    filename2 = "%s/%s" %(directory, "f_ct_cl_st_sl_tp_prt_em_im_wl.csv")

    f2 = open(filename2, "a+")

    line2 = line.strip().split(",")

    line2 = map(str.strip,  line2)
    cattitle = line2[0]
    catlink = line2[1]
    subcattitle = line2[2]
    subcatlink = line2[3]
    tpe = line2[4]
    prt = line2[5]
    wl = line2[6]
    img = line2[7]

    driver = phan_proxy.main(wl)
     
    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

    except WebDriverException:
        pass

    page = driver.page_source
    tree = html.fromstring(page)

    embedlink =  tree.xpath("/html/body/div[2]/center/div/div/div[2]/iframe/@src")
    embedlink2 =  tree.xpath("/html/body/object/embed/@src")
    embedlink3 =  tree.xpath("/html/body/div[2]/center/div/div/div[2]/object/embed/@src")

    if embedlink  is not None:
        print >>f2, ','.join([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink[0]).strip(), img,  wl])
        logging.debug([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink[0]).strip(), img,  wl])

    elif embedlink2 is not None:
        print >>f2, ','.join([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink2[0]).strip(), img,  wl])
        logging.debug([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink2[0]).strip(), img,  wl])

    elif embedlink3 is  not None:
        print >>f2, ','.join([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink3[0]).strip(), img,  wl])
        logging.debug([cattitle, catlink, subcattitle, subcatlink, tpe, prt, str(embedlink3[0]).strip(), img,  wl])

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
    f = open("to_extract_cat.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_ct_cl_st_sl_vt_wp_wl_img.txt")

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
#    line = "tv-shows-and-awards,http://www.filmlinks4u.net/category/tv-shows-and-awards,IIFA Awards (2013),http://www.filmlinks4u.net/2013/08/iifa-awards-2013.html, - ,Watch Online Part 1,http://nobuffer.info/nv.php?url=rgx25fd5a77tv,http://www.filmlinks4u.net/wp-content/uploads/2013/08/IIFA-Awards-2013.jpg"

#    main(line)
    mainthreading()
