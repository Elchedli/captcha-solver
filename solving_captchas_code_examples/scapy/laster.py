import scrapy
class WikiSpider(scrapy.Spider):
    name = "wiki"
    start_urls = ["https://en.wikipedia.org/wiki/Scrapy"]
    def parse(self, response):
        sel = scrapy.Selector(response)
        sites = sel.xpath('//body/div')
        for site in sites:
            title = site.xpath('//h1/text()').extract()
            subtitle = site.xpath('//h2/span/text()').extract()
            bold = site.xpath('//p/b').extract()
            links = site.xpath('//a/@href').extract()
            # print(title, subtitle, bold, links)

        yield {
            'title': title,
            'subtitle': subtitle,
            'bold': bold,
            'links': links,
        }

WikiSpider(scrapy)