# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymongo
from scrapy.pipelines.files import FilesPipeline
#常用的mongodb保存方法，以后可以来这里copy

class WandoujiaPipeline(object):

    def __init__(self,mongo_url,mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].update_one(item,{'$set':item},upsert=True)
        return item

    def close_spider(self,spider):
        self.client.close()

class MyFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):

        size = item['size']
        realsize = 30
        if item['size'].endswith('KB'):
            realsize = float(item['size'][:-2]) / 1024
        if item['size'].endswith('MB'):
            realsize = float(item['size'][:-2])
        if item['size'].endswith('GB'):
            realsize = float(item['size'][:-2]) * 1024

        if realsize <= 20:
            dict = {'data_app_id' : item['data_app_id'],
                    'data_app_vname' : item['data_app_vname'],
                    'year' : item['year']}
            yield scrapy.Request(item['download_url'], meta = dict)

    def file_path(self, request, response=None, info=None):
        meta = request.meta;
        return '/' + meta['year'] + '/' + meta['data_app_id'] + 'v' + meta['data_app_vname']
