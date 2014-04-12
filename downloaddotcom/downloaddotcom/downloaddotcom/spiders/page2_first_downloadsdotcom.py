import ast
import req_proxy
from bs4 import BeautifulSoup
import sys 
import os 
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
from lxml import html 

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 100
enclosure_queue = multiprocessing.JoinableQueue()




class pl_to_info(object):
   
   def __init__(self, line):
       line = str(line).strip()
       self.line_list = ast.literal_eval(line)
       f = open("to_extract_downloads")
       self.direc = f.read().strip()
       f.close()




   def pl_to_info_collection(self):
       tl = self.line_list[0]
       tt = self.line_list[1]
       cl = self.line_list[2]
       ct = self.line_list[3]
       pl = self.line_list[4]

       page = req_proxy.main(pl)
       soup = BeautifulSoup(page, "html.parser")
       
       pt = soup.find("h1", attrs= {"itemprop":"name"})
       pt = pt.get_text().encode("ascii", "ignore")

       version = soup.find("li", attrs={"class":"qsVersion"})
       version = version.get_text().encode("ascii", "ignore")

       filesize = soup.find("li", attrs={"class":"fileSize"})
       filesize = filesize.get_text().encode("ascii", "ignore")

       dtadded = soup.find("li", attrs={"class":"qsDateAdded"})
       dtadded = dtadded.get_text().encode("ascii", "ignore")

       price = soup.find("li", attrs={"class":"qsPrice"})
       price = price.get_text().encode("ascii", "ignore")

       oosys = soup.find("li", attrs={"class":"qsOs"})
       oosys = oosys.get_text().encode("ascii", "ignore")

       tdown = soup.find("li", attrs={"class":"qsTotalDownloads"})
       tdown = tdown.get_text().encode("ascii", "ignore")

       wkdown = soup.find("li", attrs={"class":"qsWeeklyDownloads"})
       wkdown = wkdown.get_text().encode("ascii", "ignore")

       direc2 = "%s/%s/%s" %(self.direc, tt, ct)

       try:
           os.makedirs(direc2)
       except:
           pass

       filename = "%s/%s.csv" %(direc2, ct)

       f = open(filename, "a+")

       info = map(self.mystrip, [tl, tt, cl, ct, pl, pt, version, filesize, dtadded, price, oosys, tdown, wkdown])
       logging.debug(info)
       
       infostr = ','.join(info)
       f.write(infostr + "\n")

       f.close()
       



   def mystrip(self, stringline):
       return str(stringline).replace("\n" , " ").replace("\t", " ").replace("\r", " ").replace(",",  " ")

       


def supermain2(i, q):
    for  line in iter(q.get, None):
        try:
            obj = pl_to_info(line)
            obj.pl_to_info_collection()

        except:
            f = open("page2_first_error_download.txt", "a+")
            f.write(line + "\n")
            f.close()

        time.sleep(2)
        q.task_done()

    q.task_done()



def supermain():
    f = open("to_extract_downloads")
    directory = f.read().strip()
    f.close()

    filename = "%s/ln_cl_ct_pl.txt" %(directory)

    fm = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=supermain2, args=(i, enclosure_queue,)))
        #procs.append(Thread(target=supermain2 , args=(i, enclosure_queue,)))
        procs[-1].start()


    for  line  in fm:
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

    fm.close()
    


if __name__=="__main__":
    supermain()
       
