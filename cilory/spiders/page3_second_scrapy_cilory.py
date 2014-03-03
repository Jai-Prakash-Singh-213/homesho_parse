# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import time

#page3_scrapy_myntra.py , page3_filedivision_myntra.py 

class DmozSpider(Spider):
    name = "link_to_link"
    allowed_domains = ["cilory.com"]
 
    def __init__(self, pth = None):
       
        pthdoc = pth.strip()[:-1]
        
        pth2 = str(pth).strip().split("/")
         
        f = open(pthdoc)
	line = f.readline().strip()
	f.close()
        
	linelist = line.split(",")
	self.subcat = "None"

        self.catlink = linelist[3]

	brand = linelist[-1].strip()
        brand = brand.split("(")
        brand = str(brand[0]).strip()
        self.brand = brand

        self.pth = pth        
        self.pth2 = pth2 
        self.target = str(linelist[1]).strip()

	category = str(linelist[4]).strip()
        category = category.split("(")   
        category = str(category[0]).strip()
        self.category = category
        

        f = open(pth)
	avalurls = f.read().strip().split("\n")
        self.start_urls = map(str.strip, avalurls)
	f.close()
    

    def parse(self, response):
        #sel = Selector(response)
        #title = sel.xpath("/html/body/div/div[2]/section/div[2]/div/div/div[2]/div/div/h1/text()").extract()
        #title = 
        try:
            link = response.url

            page = response.body 

	    soup = BeautifulSoup(page)
 
            title = soup.find("span", attrs={"itemprop":"name"})
            title = str(title.get_text()).strip()

            sp = soup.find("span", attrs={"id":"our_price_display"})
            sp = "Rs. %s" %(str(sp.get_text()).strip())

            mrp = soup.find("span", attrs={"id":"old_price_display"})

	    if mrp:
                mrp = str(mrp.get_text()).strip()

	    else:
	        mrp = sp 



            try:
                size  = soup.find("div", attrs={"class":"attribute_list"})
                size = size.option.get("title").strip()
            except:
                size = "None"


            vender = self.brand
 
            spec = soup.find("div", attrs={"id":"productInfo"})
            spec = str(spec).replace("\n", " ").replace("\t" ," ").replace("\r", " ").replace('"', "'")
         
 
            image = soup.find("img", attrs={"id":"bigpic"})

            if not image:
                image = soup.find("img", attrs={"itemprop":"image"})

            image = str(image.get("src")).strip()

            sku = soup.find("span", attrs={"itemprop":"sku"})
            sku = str(sku.get_text()).strip()
      

            colour = soup.find("ul", attrs={"id":"color_to_pick_list"})
            colour = str(colour.li.a.get("title")).strip()
          
            desc = soup.find("div", attrs={"id":"idTab1"})
            desc = str(desc).replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
           

	    target = self.target
	    category = self.category 
	    subcat  = self.subcat 
 	    brand   = self.brand 
            metatitle = "None"
            metadisc = "None"
	    catlink = self.catlink      

            date = str(time.strftime("%d:%m:%Y"))
            status = "None"

            directory = '/'.join(self.pth2[:-1])

            filename = "%s/%s%s" %(directory , self.pth2[-1][:-5],  ".csv")

            f = open(filename, "a+")
	    print>>f,  ','.join([sku, title, catlink, sp, category, subcat, brand, image, mrp, 
	                colour, target, link, vender, metatitle, metadisc, size,
		        desc, spec, date, status])

            print [sku, title, catlink, sp, category, subcat, brand, image, mrp, 
                        colour, target, link, vender, metatitle, metadisc, size,
                        desc, spec, date, status]
            f.close()

            print[link, "ok"]


        except:
           f = open("to_scrape_once_again", "a+")
           print >>f, str(self.pth), str(response.url)
           f.close()

        
