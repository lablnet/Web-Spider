"""web_spider.py: Core of this project."""
__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Production"

from urllib.request import urlopen
from .helper import *
from .image_finder import ImageFinder
from .link_finder import LinkFinder


class WebSpider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        WebSpider.project_name = project_name
        WebSpider.base_url = base_url
        WebSpider.domain_name = domain_name
        WebSpider.queue_file = WebSpider.project_name + '/queue.txt'
        WebSpider.crawled_file = WebSpider.project_name + '/crawled.txt'
        WebSpider.boot()
        WebSpider.crawlPage('First spider', WebSpider.base_url)

    # Boot the Spider
    @staticmethod
    def boot():
        create_directory(WebSpider.project_name)
        create_files(WebSpider.project_name, WebSpider.base_url)
        WebSpider.queue = file_to_set(WebSpider.queue_file)
        WebSpider.crawled = file_to_set(WebSpider.crawled_file)

    # Let's Crawl the page
    @staticmethod
    def crawlPage(thread_name, page_url):
        if page_url not in WebSpider.crawled:
            # Update user display.
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(WebSpider.queue)) + ' | Crawled  ' + str(len(WebSpider.crawled)))
            WebSpider.addLinksToQueue(WebSpider.getLinks(page_url))
            WebSpider.queue.remove(page_url)
            WebSpider.crawled.add(page_url)
            WebSpider.updateFiles()

    # Get the links.
    @staticmethod
    def getLinks(page_url):
        HTML = WebSpider.getHTML(page_url)
        finder = LinkFinder(WebSpider.base_url)
        if HTML != "":
            finder.feed(HTML)
            return finder.getURLs()
        else:
            return set()

    # Get the HTML from valid page.
    @staticmethod
    def getHTML(page_url):
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                return html_bytes.decode("utf-8")
        except Exception as e:
            print(str(e))
            return ""
        return ""

    # Saves queue data
    @staticmethod
    def addLinksToQueue(links):
        for url in links:
            if (url in WebSpider.queue) or (url in WebSpider.crawled):
                continue
            if WebSpider.domain_name != get_domain_name(url):
                continue
            WebSpider.queue.add(url)

    # Update content in files
    @staticmethod
    def updateFiles():
        set_to_file(WebSpider.queue, WebSpider.queue_file)
        set_to_file(WebSpider.crawled, WebSpider.crawled_file)
