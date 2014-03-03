#!/usr/bin/env python 
import phan_proxy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import logging
import time 
import os 


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)




def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass




def main(line):

    
    line2 = line.split(",")
    link = line2[0].strip()

    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    menudir = line2[1].strip()
    catdir = line2[4].strip().split("(")[0].strip()
    branddir = line2[-1].strip().split("(")[0].strip()

    req_dir = "%s/%s/%s/%s" %(directory, menudir, catdir, branddir)

    try:
        os.makedirs(req_dir)
    except:
        pass
    
    driver = phan_proxy.main(link)

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

    catid = line2[2].strip()
 
    try:
        driver.find_element_by_id(catid).click()
    except WebDriverException:
        pass    

    try:
        WebDriverWait(driver,1000).until( ajax_complete,  "Timeout waiting for page to load")
    except WebDriverException:
        pass

    brandid = line2[-3].strip()

    try:
        driver.find_element_by_id(brandid).click()
    except WebDriverException:
        pass

    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
    except WebDriverException:
        pass

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

    page = driver.page_source
    #print page
    soup = BeautifulSoup(page)
    
    try:  
        tag_ul_product = soup.find("ul", attrs={"id":"product_list"})
        #print tag_ul_product 
        tag_a = tag_ul_product.find_all("a", attrs={"class":"product_img_link prodlink"})
    except:
        tag_a = []

    filename = "%s/%s.doc" %(req_dir, branddir)
    filename2 = "%s/%s.docx" %(req_dir, branddir)

    f = open(filename, "a+")
    f2 = open(filename2, "a+")

    for al in tag_a:
        print>>f,  str(line).strip(), ",", str(al.get("href")).strip()
        print >>f2,str(al.get("href")).strip() 
        logging.debug((line, al.get("href")))

    driver.delete_all_cookies()
    driver.quit()
    f.close()
    f2.close()
    

if __name__=="__main__":
    line = """ http://www.cilory.com/12-family-planning,Sexual Wellbeing,layered_category_34,http://www.cilory.com/12-sexual-wellbeing/categories-exotic_gift_packs,Exotic Gift Packs (1),layered_manufacturer_5,http://www.cilory.com/12-sexual-wellbeing/categories-exotic_gift_packs/manufacturer-kamasutra,Kamasutra (1)"""
    main(line)
