import scrapy
from scrapy.http import HtmlResponse
from bookpars.items import BookparsItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']

    def parse(self, response):
        book_links = response.xpath("//a[@class='product-title-link']/@href").extract()

        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath("//div[@class = 'pagination-next']/a[@class='pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        price_min = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        link = response.url
        rate = response.xpath("//div[@id='rate']/text()").extract_first()
        yield BookparsItem(name=name, price=price, price_min=price_min, link=link, rate=rate)
