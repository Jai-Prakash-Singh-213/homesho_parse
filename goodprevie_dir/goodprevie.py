#!/usr/bin/python

import MySQLdb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from bs4 import BeautifulSoup
from lxml import html
import sys 
import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)



def ajax_complete(driver):
    try:
        time.sleep(0.5)
        return 0 == driver.execute_script("return jQuery.active")
        
    except WebDriverException:
        pass



def main():
    link = "http://goodpreview.info/ersadmin/index.php?function_to_run=displayLoginForm"
    driver = webdriver.PhantomJS()
    driver.get(link)
    driver.implicitly_wait(30)

    username = "ajay"
    pass_word = "click@321"

    elem_username = driver.find_element_by_id("username")
    elem_username.send_keys(username)
    elem_pass = driver.find_element_by_id("password")
    elem_pass.send_keys(pass_word)
    elem_pass.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

    except WebDriverException:
        pass

    elem_simple = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/ul/li[2]/a")
    elem_simple.click()
    
    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

    except WebDriverException:
        pass

    elem_lsitdir = driver.find_element_by_xpath("/html/body/div/div[3]/div/div[3]/div[2]/h2/a")
    elem_lsitdir.click()

    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

    except WebDriverException:
        pass

    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    simploption2  = soup.find("table", attrs={"class":"simpleoptions2"})
    simpleinfo = simploption2.find_all("tr", style=re.compile("background-color"))

    db = MySQLdb.connect("localhost","root","6Tresxcvbhy","goodpreview")
    cursor = db.cursor()

    sql = """CREATE TABLE  IF NOT EXISTS goodprevietable (dt_date timestamp on update current_timestamp not null, \
                                                          redirect_link varchar(255) not null, \
                                                          redirectsite varchar(100), \
                                                          clicks varchar(100) default 0 ,\
                                                          newclick varchar(50),\
                                                          difrnce varchar(50) default 0)"""
    try:
        cursor.execute(sql)
    except:
        pass
    
    for tds in  simpleinfo[::2]:
        sitelink = tds.find("a", attrs={"class":"test_link"})
        if sitelink is not None:
            default  = sitelink.find_next()
            link_type = default.find_next()
            clk = link_type.find_next()
            sitelink2 = str(sitelink.get_text()).strip()
            sitelinktitle  = str(sitelink.get("href")).strip()
            category = str(default.get_text()).strip()   
            link_type = str(link_type.get_text()).strip()  
            newclicks = str(clk.get_text()).strip() 
             
            sql = """insert into goodprevietable (redirect_link, redirectsite, newclick) \
                                          values ("%s","%s", "%s")""" %(sitelink2, sitelinktitle, 
                                                                                    newclicks)
           
            cursor.execute(sql)
            db.commit()

            
    db.close()
    driver.delete_all_cookies()
    driver.quit()
   
    


if __name__=="__main__":
    main()


   
