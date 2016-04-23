import gevent
from gevent.queue import *
import gevent.monkey
from timeit import default_timer as timer
import random
gevent.monkey.patch_all()
from progress.bar import IncrementalBar
import requests

workers = 4
file_in = "urls.txt"


def sub_worker(task):
    r = requests.get(task)
    html = r.text

    

def worker():
    while not q.empty():
        task = q.get()
        try:
            sub_worker(task)
        finally:
            bar.next()
            gevent.sleep(random.uniform(0.001,0.005))
            #q.task_done()

def loader():
    with open(file_in, "r") as text_file:
        for line in text_file:
            if len(line.strip()) > 1:
                q.put(line.strip(), timeout=3)

                     

def asynchronous():
    threads = []
    for i in range(0, workers):
        threads.append(gevent.spawn(worker))
    start = timer()
    gevent.joinall(threads,raise_error=True)
    end = timer()
    bar.finish()
    print ""
    print "Time passed: " + str(end - start)[:6]

q = gevent.queue.JoinableQueue()
gevent.spawn(loader).join()
bar = IncrementalBar('Processing', max=q.qsize())
asynchronous()

