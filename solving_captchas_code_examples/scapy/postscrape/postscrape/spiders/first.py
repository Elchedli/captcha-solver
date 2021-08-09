import scrapy
from scrapy.utils.response import open_in_browser
class WikiSpider(scrapy.Spider):
    name = "wiki"
    start_urls = ["https://en.wikipedia.org/wiki/Scrapy"]
    # print(start_urls)
    def parse(self, response):
        open_in_browser(response)
        # open_in_browser(response)