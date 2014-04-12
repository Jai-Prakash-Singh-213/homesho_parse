# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import time
from lxml import html
import re
import ast

#page3_scrapy_myntra.py , page3_filedivision_myntra.py 

class DmozSpider(BaseSpider):
    name = "link_to_link"
    allowed_domains = ["amazon.in"]

    def __init__(self, pth = None):
        self.pth = pth

        pthdoc = pth.strip()[:-1]

        f = open(pthdoc)
        line = f.readline().strip()
        f.close()

        line = line.strip()
        line = ast.literal_eval(line)

        self.target = line[0]
        self.catlink = line[1]
        cattitle = line[2]
        start = cattitle.find("(")
        self.cattitle = cattitle[:start].strip()
        self.scatlink = line[3]
        scattitle = line[4]
        start = scattitle.find("(")
        self.scattitle = scattitle[:start].strip()
        self.bl = line[-4]  
        self.bt = line[-3]
        self.pl = line[-2]
        self.image = line[-1]

        f = open(pth)
        avalurls = f.read().strip().split("\n")
        self.start_urls = map(str.strip, avalurls)
        f.close()


    def mystrip(self, x):
        return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace(",", " ").strip()
    

    def parse(self, response):
        try:
            link = response.url

            page = response.body

            soup = BeautifulSoup(page, "html.parser")
             
            title = soup.find("span", attrs={"id":"btAsinTitle"}) 
            title = str(title.get_text())

            sp = "None"
            

	    try:
                sp = soup.find("b", attrs={"class":"priceLarge"})
                sp = str(sp.get_text().encode("ascii", "ignore"))
            except:
                sp = soup.find("span", attrs={"class":"price"})
	        sp = str(sp.get_text().encode("ascii", "ignore"))
	    else:
	        sp = "None"

            mrp = soup.find("span", attrs={"id":"listPriceValue"})

            if mrp is not None:
                mrp = str(mrp.get_text().encode("ascii", "ignore"))

            else:
                mrp = sp

            techdetail = soup.find("div", attrs={"class":"technicalProductFeaturesATF"})
            techdetail = str(techdetail)
            size = techdetail

            vender = []
            tag_vender = soup.find("span", attrs={"class":"availGreen"})
            tag_vender2 = tag_vender.find_parent("div")
	    tag_vender_a = tag_vender2.find_all("a")
            for al in tag_vender_a:
	        vender.append(al)

	    vender = str(vender)

            tag_desc = soup.find("div", attrs={"id":"productDescription"})
            desc = str(tag_desc)
               
            brand = self.bt

            start  = link.find("dp/")
            end = link.find("/", start+3)
            sku = str(link[start+3: end])
            
            image = self.image

            colour = "self Colour"
            
            tag_colour = soup.find("span", text=re.compile("Color"))

            if tag_colour is not None:
                colour = tag_colour.get_text() 

            spec = "None"

            tag_spec = soup.find("div", attrs={"id":"techSpecSoftlinesWrap"})

            if tag_spec is not None:
                spec = str(tag_spec)

            target = self.target
            category = self.cattitle
            subcat  = self.scattitle
            
            metatitle = soup.find("meta", attrs={"name":"title"})
            metatitle = metatitle.get("content")

            metadisc = soup.find("meta", attrs={"name":"description"})
            metadisc = str(metadisc.get("content"))

            catlink = self.catlink

            date = str(time.strftime("%d:%m:%Y"))

            status = "None"

            filename = "%s.csv" %(self.pth[:-5])

            fileinput = [sku, title, catlink, sp, category, subcat, brand, image, mrp,
                         colour, target, link, vender, metatitle, metadisc, size,
                         desc, spec, date, status]

            fileinput = map(self.mystrip, fileinput)

            f = open(filename, "a+")
            print >>f,  ','.join(fileinput)
            print fileinput
            f.close()



        except:
           f = open("to_scrape_once_again_amazon", "a+")
           print >>f, str(self.pth), str(response.url)
           f.close()

