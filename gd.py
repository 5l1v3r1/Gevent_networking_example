#!/usr/bin/python
#- * -coding: utf-8 - * -

# File name: atr.py
# Author: sup3ria
# Version: 3.0
# Python Version: 2.7
import sys
import os
import time
from timeit import default_timer as timer
import imaplib
import itertools
import argparse
import random
import signal

import gevent
from gevent.queue import *
from gevent.event import Event
import gevent.monkey

def sub_worker(t):
    return t

def worker():
	try:
	    while not evt.is_set():
	        t = q.get(block=True, timeout=1)
	        print t
	        q_status.put(t)#send status
	        l = sub_worker(t)
	        gevent.sleep(random.uniform(1.50,0.6))
	       # if l:
	        q_valid.put(t)#send to write to disk
	       # if invunma:
	           # if not l:
	        q_invalid.put(t)#send to write to disk
	           # if l == "um":
	        q_unmatched.put(t)#send to write to disk
	    if evt.is_set():
			send_sentinals()
	except:
		send_sentinals()
                                
def loader():
    for i in xrange(5000):
        if evt.is_set():
            break
        else:
			q.put(i, timeout=time_out)
        
def writer_valid():
    try:
        with open(file_out, "a") as f:
            sen_count = workers
            while True:
                t =  q_valid.get(block=True)            
                if t == "SENTINAL":
                    sen_count -= 1
                    if sen_count<1:
                        break
                else:
                    f.write(str(t)+"\n") 
    except:
        pass
        
def writer_invalid():  
    try:
        with open(file_in[:-4] + "_invalid.txt", "a") as f:
            sen_count = workers
            while True:
                t = q_invalid.get(block=True)           
                if t == "SENTINAL":
                    sen_count -= 1
                    if sen_count<1:
                        break
                else:
                    f.write(str(t)+"\n") 
    except:
        pass
        
def writer_unmatched():
    try:
        with open(file_in[:-4] + "_unmatched.txt", "a") as f:
            sen_count = workers
            while True:
                t = q_unmatched.get(block=True)         
                if t == "SENTINAL":
                    sen_count -= 1
                    if sen_count<1:
                        break
                else:
                    f.write(str(t)+"\n") 
    except:
        pass
        
def state():
    sen_count = workers
    while True:
        t = q_status.get(block=True)
        if t == "SENTINAL":
            sen_count -= 1
            if sen_count<1:
                with open("last_line.log", "w") as f:
                    f.write(str(tt))  
                break
        else:
            tt = t

def send_sentinals():
    q_status.put("SENTINAL")
    q_valid.put("SENTINAL")
    if invunma:
        q_invalid.put("SENTINAL")
        q_unmatched.put("SENTINAL")
        
def handler(signum, frame):
    print "[INFO]Shutting down gracefully."
    evt.set()
                  
def asynchronous():
    threads = []
    threads.append(gevent.spawn(loader))
    for i in xrange(0, workers):
        threads.append(gevent.spawn(worker))
    threads.append(gevent.spawn(writer_valid))
    threads.append(gevent.spawn(state))
    if invunma:
        threads.append(gevent.spawn(writer_invalid))
        threads.append(gevent.spawn(writer_unmatched))
    start = timer()
    gevent.joinall(threads)
    end = timer()
    print ""
    print "[INFO]Time elapsed: " + str(end - start)[:5], "seconds."
    evt.set()#cleaning up


parser = argparse.ArgumentParser(description='Atlantr Imap Checker v3.0')
parser.add_argument(
    '-i',
    '--input',
    help="Inputfile",
    required=False,
    type=str,
    default="email_pass.txt")
parser.add_argument(
    '-o',
    '--output',
    help='Outputfile',
    required=False,
    type=str,
    default="mail_pass_valid.txt")
parser.add_argument(
    '-t',
    '--threads',
    help='Number of Greenlets spawned',
    required=False,
    type=int,
    default="1000")
parser.add_argument(
    '-uh',
    '--unknownhosts',
    help='Check for unknown hosts',
    required=False,
    type=bool,
    default=False)
parser.add_argument(
    '-gm',
    '--ghostmode',
    help='Continues linecount without userinput',
    required=False,
    type=bool,
    default=False)
parser.add_argument(
    '-iu',
    '--invunma',
    help='Log invalid an unmatched accounts.',
    required=False,
    type=bool,
    default=True)   
parser.add_argument(
    '-g',
    '--grabber',
    help='Grab for matchers.',
    required=False,
    type=bool,
    default=True)
parser.add_argument(
    '-mf',
    '--matchfile',
    help='File with matchers..',
    required=False,
    type=str,
    default="matchers.dat")
parser.add_argument(
    '-to',
    '--timeout',
    help='timeout in sec',
    required=False,
    type=float,
    default="0.1")
    
args = vars(parser.parse_args())

file_in = args['input']
file_out = args['output']
workers = args['threads']
phosts = args['unknownhosts']
ghsme = args['ghostmode']
invunma = args['invunma']
grabactiv = args['grabber']
file_match = args['matchfile']
time_out = args['timeout']

gevent.monkey.patch_all()

evt = Event()
signal.signal(signal.SIGINT, handler)

q = gevent.queue.Queue(maxsize=5000) #loader
q_valid = gevent.queue.Queue()#valid
q_status = gevent.queue.Queue()#status
if invunma:
    q_invalid = gevent.queue.Queue()#invalid
    q_unmatched = gevent.queue.Queue()#unmatched
asynchronous()
