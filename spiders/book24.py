import scrapy
from scrapy.http import HtmlResponse
from bookpars.items import BookparsItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=python']

    def parse(self, response):
        book_links = response.xpath("//a[@class='book-preview__title-link']/@href").extract()

        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath(
            "//a[@class='catalog-pagination__item _text js-pagination-catalog-item' and text()='Далее']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        autor_a = response.xpath(
            "//span[contains(text(),'Автор')]/ancestor::div[@class='item-tab__chars-item']//a/text()").extract_first()
        autor_meta = response.xpath(
            "//span[contains(text(),'Автор')]/ancestor::div[@class='item-tab__chars-item']//meta/@content").extract_first()
        price = response.xpath("//div[@class = 'item-actions__price-old']/text()").extract_first()
        price_min = response.xpath("//b[@itemprop]/text()").extract_first()
        link = response.url
        rate = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()
        yield BookparsItem(name=name, price=price, price_min=price_min, link=link, rate=rate, autor_a=autor_a,
                           autor_meta=autor_meta)

        # //span[contains(text(),'Автор')]/ancestor::div[@class='item-tab__chars-item']
