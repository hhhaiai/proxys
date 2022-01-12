from urllib import parse

import redis
import scrapy
from scrapy_redis.spiders import RedisSpider

from wanDouJia.items import WandoujiaItem

# 全局变量，用于设定默认值
default_value = "null"
# 豌豆荚爬虫
class WanDouJiaSpider(RedisSpider):
    # 爬虫命名
    name = "WanDouJiaSpider"
    redis_key = "WanDouJiaSpider:start_urls"
    # 初始化
    def __init__(self):
        # 基础url
        self.base_url = "https://www.wandoujia.com/search?key={}"
        # 下一页的请求
        self.next_page_url = "https://www.wandoujia.com/search?key={0}&page=2&source=index"
        self.headers = {
            "Host": "www.wandoujia.com",
            "Referer": "https://www.wandoujia.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
        }
    # 根据关键字构建请求
    def start_requests(self):
        """
        从redis之中读取关键字拼接出url
        :return:
        """
        connect = redis.Redis(host='127.0.0.1', port=6379, db=5, password='pengfeiQDS')  # 获取redis数据库连接对象
        keyword_total = connect.dbsize()  # 获取redis数据库关键字总数量
        # 遍历获取每一个关键字
        #for index in range(210001,240001):
        for index in range(1480001,1600001):
            keyword = connect.get(str(index)).decode('utf-8')  # 使用get方法获取关键字
            print("查看获取的关键字：", keyword)
            target_url = self.base_url.format(parse.quote(keyword))
            # 将拼接后的url加入爬取队列
            yield scrapy.Request(url=target_url, callback=self.get_page, meta={'keyword': keyword})
    # 解析获取的页面
    def get_page(self,response):
        # 判断是否响应成功
        if response.status == 200:
            print("查看获取的页面：",response.text)
            # 从中选出li标签
            info_list = response.xpath('//li[@class="search-item search-searchitems"]')
            print(info_list)
            # 获取当期搜索的关键字
            keyword = response.meta['keyword']
            print("查看搜索页面的关键字======================================================：",keyword)
            # 获取判断是否下一页的依据
            next_page = response.xpath('//div[@class="pagination"]//a[3]/@href')
            for info in info_list:
                print("这是获取的信息：", info)
                # 获取详情页链接
                detail_page_url = info.xpath('a/@href').extract_first()
                print(detail_page_url)
                # 加入采集队列
                yield scrapy.Request(url=detail_page_url, callback=self.get_detail_page, meta={'keyword': keyword})
            # 判断下一页的请求，因为只能请求两夜的数据，故只构造出第二页的请求
            if next_page:
                print("进入条件判断语句=======================================================")
                yield scrapy.Request(url=self.next_page_url.format(keyword), callback=self.get_page, meta={'keyword': keyword})
    # 解析详情页
    def get_detail_page(self,response):
        if response.status == 200:
            # 创建item对象
            item = WandoujiaItem()
            print("查看当前的url:", response.url)
            print("查看获取的响应页面：", response.text)
            # 解析页面获取目标字段信息
            # 当前关键字
            # APP名称
            app_name = response.xpath('//div[@class="app-info"]/p[@class="app-name"]/span/text()').extract_first()
            print("查看获取的APP名称：", app_name)
            # APP 描述
            app_desc = response.xpath('//div[@class="desc-info"]/div[@class="con"]/div[1]/text()').extract_first()
            # 发布时间
            publish_time = response.xpath('//div[@class="num-list"]/span[@class="verified-info"]/span/text()').extract_first()
            print("查看获取的APP发布时间：", publish_time)
            # 开发者
            author = response.xpath('//div[@class="infos"]/dl/dd[5]/span/text()').extract_first()
            print("查看获取的APP作者：", author)
            # 下载次数
            userDownloads = response.xpath(
                '//div[@class="num-list"]/div[@class="app-info-data"]/span/i/text()').extract_first()
            print("查看获取的APP用户下载量：", userDownloads)
            # APP图片地址
            img_url = response.xpath('//div[@class="app-icon"]/img/@src').extract_first()
            print("查看获取的APP图片地址：", img_url)
            # APP详情页链接
            detail_page = response.url
            print("查看获取的APP详情页链接：", detail_page)
            # APP分类
            category = response.xpath('//div[@class="infos"]/dl/dd[2]/a/text()').extract()
            print("查看获取的APP种类：", category)
            # APP大小
            file_size = response.xpath('//div[@class="infos"]/dl/dd[1]/text()').extract_first()
            print("查看获取的APP大小：", file_size)
            # 版本号,需要去掉空格
            version = response.xpath('//div[@class="infos"]/dl/dd[3]/text()').extract_first()
            print("查看获取的APP版本号：", version)
            # 用户好评
            item_love= response.xpath('//div[@class="num-list"]/div[@class="app-info-data"]/span[@class="item love"]/i/text()').extract_first()
            print("查看用户好评度：", item_love)
            # APP评论
            comment_num = response.xpath('//div[@class="num-list"]/div[@class="app-info-data"]/a/i/text()').extract_first()
            print("查看APP评论数：", comment_num)
            # 判断是否为空，不为空则赋值
            item['keyword'] = (response.meta['keyword']).strip()
            item['app_name'] = app_name if app_name else default_value  # APP名称
            item['app_desc'] = "".join((app_desc.split())) if app_desc else default_value   # APP描述
            item['publish_time'] = '-'.join((publish_time[-10:]).split("/")) if publish_time else default_value  # APP上线时间
            item['author'] = author if author else default_value    # APP开发者
            item['userDownloads'] = userDownloads if userDownloads else default_value   # APP下载量
            item['img_url'] = img_url if img_url else default_value  # APP图片
            item['detail_page'] = detail_page if detail_page else default_value     # APP详情页
            item['category'] = ' '.join(category) if category else default_value   # 两个种类时需要将列表项拼接在一起
            item['file_size'] = file_size if file_size else default_value   # APP大小
            item['version'] = version.strip() if version else default_value  # APP版本
            item['item_love'] = item_love if item_love else default_value   # APP评分
            item['comment_num'] = comment_num if comment_num else default_value  # APP评论数
            yield item
