import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'thehindu'
HOMEPAGE = 'https://www.thehindu.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4
queue = Queue()

Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

#Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

#Do the next job in the queue
def work():
    stop = 0
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        if queue.qsize() > 0:
            queue.task_done()
        stop += 1
        if stop == 100 :
            queue.mutex.acquire()
            queue.queue.clear()
            delete_file_contents(QUEUE_FILE)
            queue.all_tasks_done.notify_all()
            queue.unfinished_tasks = 0
            queue.mutex.release()
            return

#Each queued links is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()
    
#Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue ')
        create_jobs()
       
create_workers()
crawl()

print('The articles that has high relevance with its corresponding scores are : ')
sorted_s = sorted(Spider.scores.items(), key=lambda kv: kv[1])
for x in sorted_s[:-6:-1]:
    print(x)
