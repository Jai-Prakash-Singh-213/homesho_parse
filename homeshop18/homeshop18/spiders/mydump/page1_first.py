#!/usr/bin/env python 

import req_proxy 
from bs4 import BeautifulSoup
from urlparse import urlparse
import re

def main3(link):

    page = req_proxy.main(link)
    
    soup = BeautifulSoup(page)
      
    tag_first_container  = soup.find("div", attrs= {"class":"filter-container first"})

    
    tag_div_cat = soup.find("div", text = re.compile("categories"))

    if tag_div_cat:
        return tag_first_container

    else:
        pass




def main2(patter_firstpage):
    for menulist in patter_firstpage:
        print menulist[1]




def main():
    link = "http://www.homeshop18.com/all-stores.html"
    page = req_proxy.main(link)

    soup = BeautifulSoup(page)

    tag_border = soup.find_all("div", attrs={"class":"border-box2 mar-top"})

    patter_firstpage = []

    for brend in tag_border:
        brend_title = brend.find("div", attrs={"class":"brend-title clearfix"}).get_text()
        cat = str(brend_title).strip()

        if  (cat == "Books") or (cat == "Jewellery"):
	    pass

	else:
	    tag_img_holder = brend.find_all("div", attrs={"class":"img-holder"})

            for sub_cat in tag_img_holder:
	        sub_cat_link = str(sub_cat.find("a").get("href")).strip()
                
                parsed = urlparse(sub_cat_link) 
		sub_cat_title = filter(None, str(parsed.path).split("/"))

	        patter_firstpage.append([cat, sub_cat_link, sub_cat_title[0].strip()])

    return patter_firstpage
 
        
def superiser():
    #patter_firstpage = main()
    #main2(patter_firstpage)

    link = "http://www.homeshop18.com/men/category:14967/inStock:true/?it_category=AS&it_action=CL-ALST01&it_label=AS-ALST01-130817150907-PR-CL-OT-OT-SC_Men&it_value=0"

    print main3(link)


if __name__=="__main__":
    superiser()
