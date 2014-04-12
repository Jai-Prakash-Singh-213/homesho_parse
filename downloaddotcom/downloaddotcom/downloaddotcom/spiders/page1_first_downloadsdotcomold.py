import time
import os 
import req_proxy
from bs4 import BeautifulSoup
from urlparse import urlparse
import multiprocessing
import logging
import time
import os
from threading import Thread
import sys


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 50
enclosure_queue = multiprocessing.JoinableQueue()



class link_cl_ct(object):
    """ this calss will open link present in list , this link containing vary first link to parse"""
    counter = 0 

    def __init__(self):
        self.link_list = ["http://download.cnet.com/windows/internet-software/?tag=rb_content;main",
	                  "http://download.cnet.com/windows/mp3-and-audio-software/?tag=rb_content;main", 
			  "http://download.cnet.com/windows/productivity-software/?tag=rb_content;main", 
			  "http://download.cnet.com/windows/screensavers-and-wallpaper/?tag=rb_content;main", 
			  "http://download.cnet.com/windows/utilities-and-operating-systems/?tag=rb_content;main"]

	self.lnk_ttl_cl_ct = []
	self.directory = "dirdownloadnet%s" %(time.strftime("%d%m%Y"))
	self.filecreation(self.directory)
        self.link_rotation(self.link_list)



    def __del__(self):
        class_name = self.__class__.__name__
        self.f.close()
        self.f2.close()



    def filecreation(self, directory):
        try:
	    os.makedirs(directory)
	except:
	    pass

	filename = "%s/ln_cl_ct.txt" %(directory)
        filename2 = "%s/ln_cl_ct_pl.txt" %(directory)
        self.f = open(filename, "w+")
        self.f2 = open(filename2, "a+")



    def link_rotation(self, link_list):
        for link in link_list:
	    self.lnk_to_cat_collecion(link)




    def lnk_to_cat_collecion(self, link):
        page = req_proxy.main(link)
        soup = BeautifulSoup(page)
        parsed = urlparse(link)
        link_path = filter(None, parsed.path.split("/"))
    
        tittl = link_path[1]
        cat_div = soup.find("dl", attrs={"class":"catNav"})
        cl_ct_list = cat_div.find_all("dd")
    
        for cl_ct in cl_ct_list:
            cl = cl_ct.a.get("href")
            cl = "%s%s" %("http://download.cnet.com", str(cl))
	    ct = str(cl_ct.a.get_text())
            print >>self.f, [link, tittl] + map(self.mystrip, [cl, ct])
            self.lnk_ttl_cl_ct.append([link, tittl] + map(self.mystrip, [cl, ct]))
       


    def mystrip(self, stringline):
        return str(stringline).replace("\n" , " ").replace("\t", " ").replace("\r", " ").replace(",",  " ")
    


    def lnk_tl_vl_vl_prl_fun(self, i, q):
        for  line in iter(q.get, None):
            #try:
            counter = 0  
            self.lnk_tl_vl_vl_prl_fun2(line, counter)

            #except:
                 

            time.sleep(2)
            q.task_done()

        q.task_done()



    def lnk_tl_vl_vl_prl_fun2(self, line, counter, cl = None):
        if cl is None:
            cl = line[-2]

        else:
            pass

        page = req_proxy.main(cl)
        soup =  BeautifulSoup(page)

	pro_div = soup.find("ul", attrs={"id":"listing-product-list"})
	pro_link = pro_div.find_all("li", attrs={"class":"listing-unit"})
       
        for pl in pro_link:
            pl = pl.find("a", attrs={"class":"OneLinkNoTx"})
            pl = pl.get("href")
            print line + [pl]
            self.f2.write(str(line + [pl]) + "\n")

        counter += len(pro_link)
        
        if counter > 1000:
            return  0

        next_url = pro_div.find("li", attrs={"class":"next"})

        try:
            next_url = "http://download.cnet.com%s" %(next_url.a.get("href"))
            logging.debug(next_url)
            self.lnk_tl_vl_vl_prl_fun2(line, counter,  next_url)
        except:
            pass
 



def supermain():
    obj  = link_cl_ct()
    obj.lnk_ttl_cl_ct
    
    procs = []

    for i in range(num_fetch_threads):
        #procs.append(multiprocessing.Process(target=obj.lnk_tl_vl_vl_prl_fun, args=(i, enclosure_queue,)))
        procs.append(Thread(target=obj.lnk_tl_vl_vl_prl_fun, args=(i, enclosure_queue,)))
        procs[-1].start()
    

    for  line  in obj.lnk_ttl_cl_ct:
        enclosure_queue.put(line)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join(2)

    print "Finished everything...."
    print "closing file...."



if __name__=="__main__":
    supermain()

    
