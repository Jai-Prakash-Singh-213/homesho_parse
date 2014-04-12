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

#page3_scrapy_myntra.py , page3_filedivision_myntra.py 

class DmozSpider(BaseSpider):
    name = "link_to_link"
    allowed_domains = ["homeshop18.com"]

    def __init__(self, pth = None):
        pthdoc = pth.strip()[:-1]

        pth2 = str(pth).strip().split("/")

        f = open(pthdoc)
        line = f.readline().strip()
        f.close()

        linelist = line.split(",")
        self.subcat = str(linelist[5]).strip()

        self.catlink = linelist[2]
        self.image = linelist[-1]
        
        brand  = linelist[-3]
        start = brand.find("-")
        self.brand = brand[start+1 : ]

        self.pth = pth
        self.pth2 = pth2

        self.target = str(linelist[3]).strip()

        category = str(linelist[3]).strip()
        self.category = category

        f = open(pth)
        avalurls = f.read().strip().split("\n")
        self.start_urls = map(str.strip, avalurls)
        f.close()
    

    def parse(self, response):
        try:
            link = response.url

            page = response.body

            soup = BeautifulSoup(page, "html.parser")
             
            tree = html.fromstring(page)
             
            title = tree.xpath("/html/body/div/div[2]/div/div/div/div[3]/div/h1/span/text()")
            title = str(title[0]).strip()
            
            sp = soup.find("span", attrs={"id":"hs18Price"})
            sp = str(sp.get_text().encode("ascii", "ignore")).strip()
            
            mrp = soup.find("em", attrs={"id":"mrpPrice"})

            if mrp:
                mrp = str(mrp.get_text().encode("ascii", "ignore")).strip()

            else:
                mrp = sp

            try:
                tag_size = soup.find("td", text=re.compile("Size"))
                size = str(tag_size.next_sibling.get_text()).strip()
                
            except:
                size = "None"

            tag_vender =soup.find("div", attrs={"class":"seller-name clearfix"})
            vender = str(tag_vender.get_text()).strip()

            tag_desc = soup.find("table", attrs={"class":"highlights-box"})
            desc = str(tag_desc).replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()

               
            brand = self.brand 

            sku = "None"
            tag_sku = soup.find("p", attrs={"class":"product-code f-left bold"})

            if tag_sku:
                sku  = str(tag_sku.get_text()).replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


            image = self.image

            colour = "None"
            
            tag_colour = soup.find("td", text=re.compile("Colour"))

            if tag_colour is not None:
                try:
                    colour = str(tag_colour.next_sibling).strip()

                except:
                    colour = str(tag_colour.find_next_sibling("td").get_text()).strip()
                    

            spec = "None"

            target = self.target
            category = self.category
            subcat  = self.subcat
            
            metatitle = "None"
            metadisc = "None"

            catlink = self.catlink

            date = str(time.strftime("%d:%m:%Y"))
            status = "None"

            directory = '/'.join(self.pth2[:-1])

            filename = "%s/%s%s" %(directory , self.pth2[-1][:-5],  ".csv")

            f = open(filename, "a+")
            print >>f,  ','.join([sku, title, catlink, sp, category, subcat, brand, image, mrp,
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
