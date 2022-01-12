# -*- coding: UTF-8 -*-

import unittest

from loguru import logger
from lxml import html
import requests
from pathlib import Path


class MyTestCase(unittest.TestCase):
    def test_xpath(self):
        page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
        tree = html.fromstring(page.content)
        # This will create a list of buyers:
        buyers = tree.xpath('//div[@title="buyer-name"]/text()')
        # This will create a list of prices
        prices = tree.xpath('//span[@class="item-price"]/text()')

        print('Buyers: ', buyers)
        print('Prices: ', prices)

    def test_path_wandujia(self):
        # content = Path('/Users/xbkaishui/work/sources/wandoujia-spider/data/alipay_detail.html').read_text()
        content = Path('/Users/xbkaishui/work/sources/wandoujia-spider/data/7062821').read_text()
        tree = html.fromstring(content)
        categories = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[2]/a/text()')
        logger.info("categories {}", ' '.join(categories))
        privacy_url = tree.xpath('//a[@class=\'privacy-link\']/@href')
        logger.info("privacy_url {}", ''.join(privacy_url))

    def test_read_from_url(self):
        url = "https://www.wandoujia.com/apps/279979";
        response = requests.get(url)
        tree = html.fromstring(response.text)
        categories = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[2]/a/text()')
        logger.info("categories {}", categories)
        privacy_url = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[5]/a/@href')
        logger.info("privacy_url {}", privacy_url)


    def test_anzhi_banks(self):
        url = " http://www.anzhi.com/pkg/ff76_com.qihuo.zhongxinsjsj.html"
        response = requests.get(url)
        tree = html.fromstring(response.text)
        categories = tree.xpath("//*[@id='detail_line_ul']/li[1]/text()")
        logger.info("categories {}", categories)
        privacy_url = tree.xpath("//*[@id='detail_line_ul']/li[9]/a/@href")
        logger.info("privacy_url {}", privacy_url)


if __name__ == '__main__':
    unittest.main()
