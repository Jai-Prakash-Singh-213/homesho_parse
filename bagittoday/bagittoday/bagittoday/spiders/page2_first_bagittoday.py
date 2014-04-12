#!/usr/bin/env python 
import ast
import req_proxy
from bs4 import BeautifulSoup
from lxml import html 
import time
import os
import multiprocessing
import logging


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 50
enclosure_queue = multiprocessing.JoinableQueue()


def string_strip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " " ).replace(",", " ").strip()


def main(line):
    line = ast.literal_eval(line)
    line = map(str.strip, line)
    target = line[0]
    catlink = line[1]
    cattitle = line[2]
    subcatlink = line[3]
    subcattitle = line[4]
    brand = line[5]
    productlink = line[6]
    imagelink = line[7]
    producttitle = line[8]

    
    f = open("to_extractbagittoday")
    directory = f.read().strip()
    f.close()

    dir2 = "%s/%s/%s/%s/%s"  %(directory, target, cattitle, subcattitle, brand)

    try:
        os.makedirs(dir2)
    except:
        pass

    filename = "%s/%s.csv" %(dir2, brand)

    f = open(filename,  "a+")
    
    page = req_proxy.main(productlink)

    soup = BeautifulSoup(page)
    
    product_path = productlink.split("/") 

    product_path = filter(None, product_path)
    sku = str(product_path[-1])
    
    start = sku.find("-")
    if start !=-1:
        sku = sku[start+1:]
 
    sp = soup.find("span", attrs={"class":"offer-price"})
    sp = str(sp.get_text())

    mrp = sp
    mrp2 = soup.find("span", attrs={"class":"mrp-price"})
    
    if mrp2 is not None:
        mrp = str(mrp2.get_text())

    colour = None

    colour2 = soup.find("span", attrs={"class":"colorClass"})

    if colour2 is not None:
        colour = str(colour2.get("title"))
 
    size = []

    size2 = soup.find("ul", attrs={"class":"attributes-ul-cont"})
    if size2 is not None:
        size2 = size2.find_all("input")
        for sz in size2:
            size.append(str(sz.get("value")))

    size = str(size)

    tree = html.fromstring(page)

    desc2 = tree.xpath("/html/body/div/section/div[4]/div/section/div/div/div/div")

    desc2 = desc2[0]
    desc = str(html.tostring(desc2))

    spec = None

    date = str(time.strftime("%d%mi%Y"))

    status =  "None"

    vender = "bagittoday.com"

    metadesc2 = soup.find("meta", attrs={"name":"description"})
    metadesc = str(metadesc2.get("content"))

    metatitle2 = soup.find("title")
    metatitle = str(metatitle2.get_text())

    output =  [sku, producttitle, catlink, sp, cattitle, subcattitle, brand, imagelink, mrp,
               colour, target, productlink, vender, metatitle, metadesc, size,
               desc, spec, date, status]

    output = map(string_strip, output)

    print >>f, ','.join(output)

    print output
   



def part_threading2(i, q):
    for  line in iter(q.get, None):
        try:
            main(line)
            print line

        except:
            f2 = open("page2_first_bagittoday_error.txt", "a+")
            print >>f2, line
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()



def part_threading():
    f = open("to_extractbagittoday")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_mn_ct_ct_scl_sct_bt.txt")

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
    line = "['Home & Kitchen', 'http://www.bagittoday.com/home-furnishing/c-232/', ' Home Furnishing', 'http://www.bagittoday.com/quilts-and-comforters/c-2212/', 'Quilts & Comforters', 'private', 'http://www.bagittoday.com/winter-mink-blanket-assorted-/pr-210397_c-2212/', 'http://images.bagittoday.com/0/images/product/210397/Winter_Mink_Blanket_Assorted_225X225_00_0.jpg', 'winter mink blanket (assorted)']"

    #main(line)

    part_threading()


