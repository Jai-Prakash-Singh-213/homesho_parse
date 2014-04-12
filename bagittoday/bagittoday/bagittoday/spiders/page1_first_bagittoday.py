#!/usr/bin/env python 
import phan_proxy
from bs4 import BeautifulSoup
import re
import profile
import time
import os 




def child_cat_extraction(child_cat_tag):
     child_link = "http://www.bagittoday.com%s" %(str(child_cat_tag.a.get("href")).strip())
     child_title = str(child_cat_tag.a.get_text().strip())

     return {child_link:child_title}




def sub_cat_extraction(sub_cat_tag):
    sub_cat_link_title = "http://www.bagittoday.com%s, %s" %(str(sub_cat_tag.a.get("href")).strip(), 
                                                             str(sub_cat_tag.a.get("title")).strip())

    child_cat = sub_cat_tag.find_all("li", id = re.compile("childCat"))

    chile_cat_likn_title = map(child_cat_extraction, child_cat)
 
    return sub_cat_link_title, chile_cat_likn_title




def main():
    directory = "dirbagittoday%s" %(time.strftime("%d%m%Y"))

    try:
        os.makedirs(directory)
    except:
        pass

    f = open("to_extractbagittoday", "w+")
    print >>f, directory
    f.close()

    f2 = open("extractedbagittoday", "a+")
    print >>f2, directory
    f2.close()

    filename = "%s/%s" %(directory, "f_mn_sl_st_scl_sct.txt")
    f = open(filename, "a+")
    
    link = "http://www.bagittoday.com/"
    driver = phan_proxy.main(link)
    driver.refresh()
    page = driver.page_source
    driver.delete_all_cookies()
    driver.quit()
 
    soup = BeautifulSoup(page)

    tag_menu = soup.find("ul", attrs={"id":"menu"})
    tag_menu_li = tag_menu.find_all("li", attrs={"class":"first"})

    req_menu = ["Men", "Women", "Kids", "Electronics & Mobiles", "Home & Kitchen", "Jewellery"]
    
    req_manu_obj = []
    
    for al in tag_menu_li:
        if  str(al.a.get_text()).strip()  in req_menu:
	    req_manu_obj.append(al)
 
    req_menu_subcat = {}
    
    for menu in  req_manu_obj:
        menu_sub_cat = menu.find_all("li", id = re.compile("subCat"))
        req_menu_subcat[str(menu.a.get_text()).strip()] = menu_sub_cat


    mn_scl_sct_ccatl_ccatt = {}

    for  k, v in req_menu_subcat.items():
         sub_cat_likn_title = map(sub_cat_extraction, v)

	 mn_scl_sct_ccatl_ccatt[k] =  sub_cat_likn_title

    #print mn_scl_sct_ccatl_ccatt

    for k, v in mn_scl_sct_ccatl_ccatt.items():
        for scl_sct_cl_ct in v:
	    sl_st = scl_sct_cl_ct[0]
            sl_st  = sl_st.split(",")
            sl = sl_st[0]
            st = sl_st[1]
            
            if scl_sct_cl_ct is None:
                print >>f, [k, sl, st, sl, st]
                print [k, sl, st, sl, st]

	    for cl_ct in scl_sct_cl_ct[1]:
	        cl = cl_ct.keys()[0]
		ct = cl_ct.values()[0]
                print >>f, [k, sl, st, cl, ct]
                print [k, sl, st, cl, ct]

    f.close()
    



def supermian():
    main()




if __name__=="__main__":
    profile.run("supermian()")

    
