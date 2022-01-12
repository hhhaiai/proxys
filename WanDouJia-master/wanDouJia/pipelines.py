# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.htmlm
from .utils import get_db
mongo_db = get_db()

class WandoujiaPipeline(object):
    # 创建文件的方法
    def open_spider(self, spider):
        """
        在当前目录下创建文件，记录采集的数据
        :param spider:
        :return:
        """
        self.file = open('./豌豆荚采集测试数据.txt', 'a+', encoding='utf-8', errors="ignore")  # 创建文件
    def process_item(self, item, spider):
        keyword = item['keyword']  # 关键字
        print("查看获取的关键字===================：", keyword)
        app_name = item['app_name']  # APP名称
        print("查看获取的APP名称==================：", app_name)
        app_desc = item['app_desc']  # APP 描述
        print("查看获取的APP描述==================：", app_desc)
        publish_time = item['publish_time']  # 发布时间
        print("查看获取的APP发布时间==============：", publish_time)
        author = item['author']  # 开发者
        print("查看获取的APP作者==================：", author)
        userDownloads = item['userDownloads']  # 下载次数
        print("查看获取的APP用户下载量============：", userDownloads)
        img_url = item['img_url']  # APP图片地址
        print("查看获取的APP图片地址==============：", img_url)
        detail_page = item['detail_page']   # APP详情页
        print("查看获取的APP详情页================：", detail_page)
        category = item['category']  # APP分类
        print("查看获取的APP作者==================：", category)
        file_size = item['file_size']  # APP大小
        print("查看获取的APP大小==================：", file_size)
        version = item['version']  # 版本号,需要去掉空格
        print("查看获取的APP版本号================：", version)
        item_love = item['item_love']  # 用户好评
        print("查看用户好评度=====================：", item_love)
        comment_num = item['comment_num']  # APP评论
        print("查看APP评论数======================：", comment_num)
        # 将采集的目标字段整理成统一格式，定义变量接收拼接的结果
        result_content = ""
        result_content = result_content.join(
            keyword + "ÿ" + app_name + "ÿ" + app_desc + "ÿ" + publish_time + "ÿ" + author + "ÿ" +
            userDownloads + "ÿ" + img_url + "ÿ" + detail_page + "ÿ" + category + "ÿ" + file_size + "ÿ" +
            version + "ÿ" + item_love + "ÿ" + comment_num + "ÿ" + "\n"
        )
        # 将采集的数据写入文件
        self.file.write(result_content)
        self.file.flush()
        return item

    # 关闭文件的方法
    def close_spider(self, spider):
        """
        将采集的数据写入文件完成后，关闭文件
        :param spider:
        :return:
        """
        # 关闭文件
        self.file.close()


# 以下代码是存储到 mongodb时需要的代码
class ResultToMongoPipeline(object):
    """抓取结果导入 mongo"""

    def __init__(self, settings):
        self.collections_name = settings.get('RESULT_COLLECTIONS_NAME')

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_item(self, item, spider):
        mongo_db[self.collections_name].insert(item)
        return item
