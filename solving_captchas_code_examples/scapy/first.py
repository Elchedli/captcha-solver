import scrapy
from scrapy.utils.response import open_in_browser
# response = scrapy.fetch("https://www.reddit.com/r/gameofthrones/")
# scrapy.view(response)
# open_in_browser(response)

class WikiSpider(scrapy.Spider):
    name = "wiki"
    start_urls = ["https://en.wikipedia.org/wiki/Scrapy"]
    print(start_urls)
    def parse(self, response):
        print(response)
        # open_in_browser(response)
        # sel = scrapy.Selector(response)
        # sites = sel.xpath('//body/div')
        # for site in sites:
        #     title = site.xpath('//h1/text()').extract()
        #     subtitle = site.xpath('//h2/span/text()').extract()
        #     bold = site.xpath('//p/b').extract()
        #     links = site.xpath('//a/@href').extract()
        #     print(title, subtitle, bold, links)


WikiSpider