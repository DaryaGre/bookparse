# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparsItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    name = scrapy.Field()
    autor = scrapy.Field()
    autor_a = scrapy.Field()
    autor_meta = scrapy.Field()
    price = scrapy.Field()
    price_min = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()
