"""main.py: Base."""
__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Production"

import threading
from queue import Queue
from web_spider import WebSpider
from helper import *

url = str(input("Enter the url to crawl: "))

domain = get_domain_name(url)
project_name = domain
queue_file =  project_name + '/queue.txt'
crawled_file = project_name + '/crawled.txt'
No_of_thread = 4

queue = Queue()
WebSpider(project_name, url, domain)


# Create worker.
def workers():
    for _ in range(No_of_thread):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in queues.s
def work():
    while True :
        url = queue.get()
        WebSpider.crawlPage(threading.current_thread().name, url)
        queue.task_done()

# Lets do the job.
def jobs():
    for link in file_to_set(queue_file):
        queue.put(link)

    queue.join()
    crawl()

# If anything left in queue, so crawl then.
def crawl():
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        # Update the user display
        print(str(len(queued_links)) + ' links in the queue')
        jobs()


def main():
    workers()
    crawl()
