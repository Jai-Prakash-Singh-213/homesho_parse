#!/usr/bin/env python 
import req_proxy
from bs4 import BeautifulSoup
from lxml import html
from Queue import Queue
from threading import Thread
import time
import logging
import os 
import phan_proxy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException



logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

num_fetch_threads = 30
enclosure_queue = Queue()




def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass




def main4(i, q):
    for line, catlink, f2 in iter(q.get, None):
        #try:
            catid = line.split(",")[-3].strip()

            #page = req_proxy.main(catlink)
            driver = phan_proxy.main(catlink)

            try:
                WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
            except WebDriverException:
                pass
            
            try:
                driver.find_element_by_id("fancybox-close").click()
            except WebDriverException:
                pass
  
            try:
                WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
            except WebDriverException:
                pass

       
            try:
                driver.find_element_by_id(catid).click()
            except WebDriverException:
                pass
    
            try:
                WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
            except WebDriverException:
                pass
 
	    page = driver.page_source
            driver.delete_all_cookies()
            driver.quit()

            soup = BeautifulSoup(page)
         
	    try:
	        tag_brand = soup.find("ul", attrs={"id":"ul_layered_manufacturer_0"})
                tag_brand_li = tag_brand.find_all("li", attrs={"class":"nomargin hiddable "})
	    except:
	        tag_brand_li = []

	    for in_a in tag_brand_li:
                bid = str(in_a.input.get("id")).strip() 
	        blinktext = in_a.find("a")
	        blink = str(blinktext.get("href")).strip()
	        btitle =str(blinktext.get_text()).strip()
                line2 = "%s,%s,%s,%s" %(line, bid, blink, btitle)
               
	        print >>f2, line2
       
                logging.debug((line2))
          
    
	    time.sleep(2)
	    q.task_done()

        #except:
        #    q.task_done()
    
    q.task_done()




def main3():
    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    f_ml_mt_cl_ct = "%s/%s" %(directory, "f_ml_mt_cl_ct.txt")
    f_ml_mt_cl_ct_bl_bt = "%s/%s" %(directory, "f_ml_mt_cl_ct_bl_bt.txt")
  
    f = open(f_ml_mt_cl_ct)
    f2 = open(f_ml_mt_cl_ct_bl_bt, "a+")

    procs = []

    for i in range(num_fetch_threads):
        procs.append(Thread(target=main4, args=(i, enclosure_queue,)))
	#worker.setDaemon(True)
	procs[-1].start()


    for line in f:
        try:
            line = line.strip()
            catlink = line.split(",")[-2].strip()

            enclosure_queue.put((line, catlink, f2))

        except:
            pass

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()

    print "closing file....."
    f.close()
    f2.close()


    


def main2(i, q):
    for menulink, menutitle, f in iter(q.get, None):
        page = req_proxy.main(menulink)
        soup = BeautifulSoup(page)

        try:
            tag_cat = soup.find("ul", attrs={"id":"ul_layered_category_0"})
            tag_cat_li = tag_cat.find_all("li", attrs={"class":"nomargin hiddable "})

        except:
            tag_cat_li = []
        
        for in_a  in tag_cat_li:
            catid = str(in_a.input.get("id")).strip()
            catlinktext = in_a.find("a")
            catlink = str(catlinktext.get("href")).strip()
            cattitle =str(catlinktext.get_text()).strip()

            line = [menulink, menutitle, catid, catlink, cattitle]
            print >>f, ','.join(line)

            logging.debug(line)

	time.sleep(i+ 2)
	q.task_done()
	
    q.task_done()
       



def main():

    directory = "dir%s" %(time.strftime("%d%m%Y"))

    try:
        os.makedirs(directory)

    except:
        pass 

    f = open("to_extract.txt", "w+")
    print >>f, directory
    f.close()

    f = open("extracted", "a+")
    print >>f, directory
    f.close()

    f_ml_mt_cl_ct = "%s/%s" %(directory, "f_ml_mt_cl_ct.txt")

    f = open(f_ml_mt_cl_ct, "a+")
    
    link = "http://www.cilory.com/"
    page = req_proxy.main(link)

    tree = html.fromstring(page)
    menuframe = tree.xpath("/html/body/div[2]/div[3]/header/div/nav/ul/li")

    menuframe2 = menuframe[1:]

    del menuframe[:]
    del menuframe


    procs = []

    for i in range(num_fetch_threads):
        procs.append(Thread(target=main2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()
    
    for menu in menuframe2:
        menulink = str(menu.xpath("a/@href")[0]).strip()
        menutitle = str(menu.xpath("a/text()")[0]).strip()
       
        enclosure_queue.put((menulink, menutitle, f))

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()
     
    print "closing file....."
    f.close()




def sunpermain():
    main()    
    main3()




if __name__=="__main__":
    sunpermain()
