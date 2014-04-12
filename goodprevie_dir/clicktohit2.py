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
import sending_main2

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)



def ajax_complete(driver):
    try:
        time.sleep(0.5)
        return 0 == driver.execute_script("return jQuery.active")
        
    except WebDriverException:
        pass



def main():
    filename = "/home/desktop/goodprevie_dir/clicktohit%s.csv" %(time.strftime("%d%m%Y"))

    dt_today = time.strftime("%d:%m:%Y")
    f = open(filename, "a+")

    link = "http://click2hit.com/ersadmin/index.php?function_to_run=displayLoginForm"
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

    db = MySQLdb.connect("localhost","root","6Tresxcvbhy","click2hit")
    cursor = db.cursor()

    f.write(','.join(["dt_today","sitetitle", "sitelink", "pre_click", "new_clicks", "difrnce"]) +"\n")


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
            clicks = str(clk.get_text()).strip() 
             
            sql  = """select * from click2hittable where redirectsite = "%s" limit 1""" %(sitelinktitle)
            cursor.execute(sql)

            results = cursor.fetchall()

            if results is None:
                sql = """insert into click2hittable (redirect_link, redirectsite, newclick) \
                                          values ("%s","%s", "%s")""" %(sitelink2, sitelinktitle,
                                                                        clicks)
                cursor.execute(sql)
                db.commit()

            for row in results:
                newclick = str(row[4]).strip()
                difrnce = int(newclick) - int(clicks)
                difrnce = str(difrnce)
                sql = """ update click2hittable set clicks="%s", newclick="%s",\
                          difrnce = "%s" where redirectsite="%s" """ %(newclick, clicks, difrnce, sitelinktitle)
                cursor.execute(sql)
                db.commit()
                f.write(','.join([dt_today, sitelink2, sitelinktitle, newclick, clicks, difrnce]) +"\n")
         
   
    f.close()         
    db.close()
    driver.delete_all_cookies()
    driver.quit()

    filename2 = [filename]
    sending_main2.supermain(filename2)

   
    

if __name__=="__main__":
    main()


  
