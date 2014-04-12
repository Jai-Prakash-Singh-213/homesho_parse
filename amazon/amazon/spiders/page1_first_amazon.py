#!/usr/bin/env python 
import req_proxy
from bs4 import BeautifulSoup
import re 
import functools
import time 
import os 




def main2(x, soup, f):
     
    tag_beauti = soup.find("h2", text=re.compile(x))
    cattitle  = str(tag_beauti.get_text()).strip()

    tag_beauti_ul = tag_beauti.find_next_sibling("ul")
    tag_beauti_ul_a = tag_beauti_ul.find_all("a")
   
    for menu_cat in tag_beauti_ul_a:
        scatlink = "%s%s" %("http://www.amazon.in", str(menu_cat.get("href")).strip())
        scattitle = str(menu_cat.get_text()).strip()

        if re.search("all", scattitle.lower()) is None:
            print >>f, [cattitle, scatlink, scattitle]

        req1 = ["Home & Kitchen", "http://www.amazon.in/Home-D%C3%83%C2%A9cor/b/ref=sd_allcat_home_decor?ie=UTF8&node=1380374031", 
                "Home & Decor"]

        req2 = ["Home & Kitchen", "http://www.amazon.in/Bedroom-Linen/b/ref=sd_allcat_bedroom_linen?ie=UTF8&node=1380447031", 
                "Bedroom Linen"]

        req3 = ["Home & Kitchen", "http://www.amazon.in/Cushions-Cushion-Covers/b/ref=sd_allcat_cushions?ie=UTF8&node=1380469031", 
                "Cushions & Cushion Covers"]
 
    print >>f,  req1
    print >>f,  req2
    print >>f,  req3




def main():

    directory = "diramazon%s" %(time.strftime("%d%m%y"))
    
    try:
        os.makedirs(directory)

    except:
        pass

    f = open("to_extract_amazon.txt", "w+")
    f.write(directory)
    f.close()

    f = open("extracted_amazon.txt", "a+")
    f.write(directory)
    f.close()

    filename = "%s/%s" %(directory, "f_mn_ctl_cat.txt")

    f = open(filename, "a+")

    link = "http://www.amazon.in/gp/site-directory/ref=sa_menu_top_fullstore"
    page = req_proxy.main(link)

    soup2 = BeautifulSoup(page)

    catlist = ["Beauty & Health", "Watches & Fashion Jewellery", "Handbags & Luggage"]

    map(functools.partial(main2, soup=soup2, f = f), catlist)

    f.close()
    


if __name__=="__main__":
    main()


