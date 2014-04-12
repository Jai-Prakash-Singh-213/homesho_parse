#!/usr/bin/env python
import ast
import phan_proxy
from bs4 import BeautifulSoup
import multiprocessing
import logging
import sys
import time
from collections import Counter
import re 
import functools



logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 50
enclosure_queue = multiprocessing.JoinableQueue()


def re_line_match(avail_brand , line):
    if re.search(avail_brand, line):
        return avail_brand
    

def driver_scroller(driver):
    height = 0
    loop = True

    while loop is True:
        logging.debug("scrolling...")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        heightnow = driver.execute_script("return $(document ).height();")

        if heightnow == height:
            loop = False

        else:
            height = heightnow
            loop = True

    return driver



def str_lower_strip(x):
    return x.lower().strip()

 
def main(line):
    line = ast.literal_eval(line)
    menu = line[0]
    catlink = line[1]
    cattitle = line[2]
    scatlink = line[3]
    scattitle = line[4]

    driver = phan_proxy.main(scatlink)
    driver = driver_scroller(driver)

    page = driver.page_source

    driver.delete_all_cookies()
    driver.quit()

    soup = BeautifulSoup(page)
    tag_brand = soup.find("ul", id="filter_Brands")

    tag_brand_li = tag_brand.find_all("li")

    tag_brand_li = tag_brand_li[1:]

    f = open("to_extractbagittoday", "a+")
    directory = f.read().strip()
    f.close()
    
    filename = "%s/%s" %(directory, "f_mn_ct_ct_scl_sct_bt.txt")
    
    f = open(filename, "a+")
    
    bt_list2 = []
    
    for bt  in tag_brand_li:
        bt_list2.append(str(bt.span.get_text()))

    bt_list = map(str_lower_strip, bt_list2)

    print bt_list

    tag_pro_image = soup.find_all("div", attrs={"class":"product-image"})

    for l in  tag_pro_image:
        product_link  = "%s%s" %("http://www.bagittoday.com", str(l.find("a").get("href")).strip())
        product_image = str(l.find("img").get("data-original")).strip()
        product_title = str(l.find("img").get("title")).lower().strip()
        #product_title_split = map(str_lower_strip, product_title.lower().split(" "))
   
        #brand = list((Counter(bt_list) & Counter(product_title_split)).elements())
        brand2 = map(functools.partial(re_line_match, line = product_title), bt_list)
  
        brand = filter(None, brand2)

        if len(brand) == 0 :
            brand = "private"

        else:
            brand = brand[0].strip()

        print >>f, [menu, catlink, cattitle, scatlink, scattitle, brand, product_link, product_image, product_title]
        print  [menu, catlink, cattitle, scatlink, scattitle, brand, product_link, product_image, product_title]
        
    f.close()




def part_threading2(i, q):
    for  line in iter(q.get, None):
        try:
            main(line)
            print line

        except:
            f2 = open("page1_second_bagittoday_error.txt", "a+")
            print >>f2, line
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()




def part_threading():
    f = open("to_extractbagittoday")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_mn_sl_st_scl_sct.txt")

    f = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=part_threading2, args=(i, enclosure_queue,)))
        procs[-1].start()

    for  line  in f:
        enclosure_queue.put(line)

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




if __name__=="__main__":
    #line = "['Women', 'http://www.bagittoday.com/personal-care-and-beauty/c-445/', ' Personal Care and Beauty', 'http://www.bagittoday.com/hair-dryer/c-2221/', 'Hair Dryer']"
    #main(line)
    part_threading()


    






    
