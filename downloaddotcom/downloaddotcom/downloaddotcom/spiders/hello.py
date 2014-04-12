#!/usr/bin/env python 
import time 


if __name__=="__main__":
    for i in xrange(200):
        time.sleep(1)
        print "hello Python "
        f = open("hellopython.txt", "a+")
        f.write("hello python")
	f.close()

