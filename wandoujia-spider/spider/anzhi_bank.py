# -*- coding: UTF-8 -*-
import csv
import time
import urllib.parse

import requests
from loguru import logger
from lxml import html

import random
from fake_useragent import UserAgent

import random


def getheaders():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    UserAgent = random.choice(user_agent_list)
    return UserAgent


def format_url(full_url):
    if len(full_url) < 2:
        return full_url
    url = urllib.parse.urlparse(full_url)
    return url.netloc


class AnZhiBankSpider(object):

    def crawl(self, banks_url_file, out_file):
        csv_file = open(out_file, 'w', newline='')
        bank_category_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        bank_category_writer.writerow(['name', 'category', 'url'])
        f = open(banks_url_file, 'r')
        lines = f.readlines()
        refer_url = 'http://www.anzhi.com/pkg/ff76_com.qihuo.zhongxinsjsj.html'
        for line in lines:
            pair = line.strip().split(",")
            url = pair[0]
            name = pair[1]
            logger.info("crawl {} url {}", name, url)
            category, url = self.crawl_one_row(url, refer_url)
            time.sleep(1)
            refer_url = url
            bank_category_writer.writerow([name, category, url])

    def crawl_one_row(self, url, refer_url):
        headers = {
            'Cookie': 'PHPSESSID=8fcc59bbcd715f6ab33422ee22138572; UM_distinctid=17d2dc14ffd2ac-0989b65c2a7ff-1c306851-13c680-17d2dc14ffe5a0; CNZZDATA3216547=cnzz_eid%3D380315033-1637144171-%26ntime%3D1637144171; Hm_lvt_b27c6e108bfe7b55832e8112042646d8=1637150184; CKISP=8fe7b23ac9f49f9c2d618c8bb906fff7%7C1637150238; Hm_lpvt_b27c6e108bfe7b55832e8112042646d8=1637150253',
            'Referer': refer_url,
            "User-Agent": getheaders(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        response = requests.get(url, headers=headers, verify=False)
        tree = html.fromstring(response.text)
        categories = tree.xpath("//*[@id='detail_line_ul']/li[1]/text()")
        logger.info("categories {}", categories)
        privacy_url = tree.xpath("//*[@id='detail_line_ul']/li[9]/a/@href")
        logger.info("privacy_url {}", privacy_url)
        return ' '.join(categories), format_url(''.join(privacy_url))
