# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WandoujiaMainItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data_app_id = scrapy.Field()
    data_app_name = scrapy.Field()
    data_app_pname = scrapy.Field()
    data_app_vname = scrapy.Field()
    download_url = scrapy.Field()
    size = scrapy.Field()
    year = scrapy.Field()
