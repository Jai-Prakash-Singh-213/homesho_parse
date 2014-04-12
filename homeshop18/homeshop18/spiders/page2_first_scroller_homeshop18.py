#!/usr/bin/env python 
import phan_proxy
from bs4 import BeautifulSoup
import logging
import time 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import multiprocessing
import os 
from urlparse import urlparse
from lxml import html

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 100
enclosure_queue = multiprocessing.JoinableQueue()

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)




def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")

    except WebDriverException:
        pass




def driver_scroller(driver):
    height = 0
    loop = True

    while loop is True:
        logging.debug("scrolling...")
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

        heightnow = driver.execute_script("return $(document ).height();")

        if heightnow == height:
            loop = False

        else:
            height = heightnow
            loop = True

    return driver




def sub_scroller(driver):
    loop = True
    while loop is True:
        try:
            print "clicking..."
            driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[3]/div/span/a/span").click()
            
            WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

        except WebDriverException:
            return driver 




def main(line):
    print line
    line2 = line.strip().split(",")
    
    menulink = line2[0].strip()
    menutitle = line2[1].strip()
  
    catlink = line2[2].strip()
    cattitle = line2[3].strip()

    subcatlink = line2[4].strip()
    subcatitle = line2[5].strip()

    brandlink = line2[6].strip()
    brandtite = line2[7].strip()

    driver = phan_proxy.main(brandlink)
   
    driver = driver_scroller(driver)    

    driver = sub_scroller(driver)

    page = driver.page_source
    
    soup = BeautifulSoup(page, "html.parser")

    tag_srchresult = soup.find("div", attrs={"id":"searchResultsDiv"})

    #tag_product = tag_srchresult.find_all("p", attrs={"class":"product_title"})
    tag_product = tag_srchresult.find_all("p", attrs={"class":"product_image"})



    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    sub_dir = "%s/%s/%s/%s/%s" %(directory, menutitle, cattitle, subcatitle, brandtite)

    try:
        os.makedirs(sub_dir)

    except:
        pass

    filename1 = "%s/%s.doc" %(sub_dir, brandtite)
    filename2 = "%s/%s.docx" %(sub_dir, brandtite)
    
    f = open(filename1, "a+")
    f2 = open(filename2, "a+")
    
    for al in tag_product:
        #prolink =  "%s%s" %("http://www.homeshop18.com", str(al.a.get("href")).strip())
        prolink =  "%s%s" %("http://www.homeshop18.com", str(al.a.get("href")).strip())
        prolimg = str(al.a.img.get("data-original")).strip()

        parsed = urlparse(prolimg)
        prolimg = "%s%s" %("http://www.homeshop18.com", parsed.path)

	print >>f, ",".join([menulink, menutitle, catlink, cattitle, subcatlink, subcatitle, brandlink,brandtite, prolink, prolimg])
        print >>f2, prolink



def part_threading2(i, q):
    for  ml_mt_ctt_ctl_sl_st_bl_bt in iter(q.get, None):
        try:
            main(ml_mt_ctt_ctl_sl_st_bl_bt)
            print  ml_mt_ctt_ctl_sl_st_bl_bt

        except:
            f2 = open("page2_first_scroller_error.txt", "a+")
            print >>f2, ml_mt_ctt_ctl_sl_st_bl_bt
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()



def part_threading():
    f = open("to_extract.txt", "a+")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_ml_mt_ctt_ctl_sl_st_bl_bt.txt")
    f = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=part_threading2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for  ml_mt_ctt_ctl_sl_st_bl_bt  in f:
        enclosure_queue.put(ml_mt_ctt_ctl_sl_st_bl_bt)

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

    print "closing file...."
    f.close()



def supermain():
     part_threading()


if __name__=="__main__":
    supermain()
