# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparsPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):

        if spider.name == 'labirint':
            if item['name'].count(': ') != 0:
                item['autor'] = item['name'].split(': ')[0]
                item['name'] = item['name'].split(': ')[1]

        if spider.name == 'book24':
            if item['price'] == None:
                item['price'] = item['price_min']
            if item['autor_a'] != None:
                item['autor'] = item['autor_a']
            elif item['autor_meta'] != None:
                item['autor'] = item['autor_meta']
            else:
                item['autor'] = None

            del item['autor_a']
            del item['autor_meta']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
