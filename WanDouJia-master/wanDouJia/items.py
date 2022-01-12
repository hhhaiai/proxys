# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WandoujiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    keyword = scrapy.Field()    # 关键字
    app_name = scrapy.Field()  # APP名称
    app_desc = scrapy.Field()   # 描述
    publish_time = scrapy.Field()   # 发布时间
    author = scrapy.Field()  # 开发者
    userDownloads = scrapy.Field()  # 下载次数
    img_url = scrapy.Field()  # APP图片地址
    detail_page = scrapy.Field()    # APP详情链接
    category = scrapy.Field()  # APP分类
    file_size = scrapy.Field()  # APP大小
    version = scrapy.Field()  # 版本号,需要去掉空格
    item_love = scrapy.Field()  # 用户好评
    comment_num = scrapy.Field()    # APP评论数






