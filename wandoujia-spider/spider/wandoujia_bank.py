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
    user_agent_list = ['Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    UserAgent=random.choice(user_agent_list)
    return UserAgent

def format_url(full_url):
    if len(full_url) < 2:
        return full_url
    url = urllib.parse.urlparse(full_url)
    # pairs = url.netloc.split('.')
    return url.netloc


class WanDouJiaBankSpider(object):

    def crawl(self, banks_url_file, out_file):
        csv_file = open(out_file, 'w', newline='')
        bank_category_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        bank_category_writer.writerow(['name', 'category', 'url'])
        f = open(banks_url_file, 'r')
        lines = f.readlines()
        refer_url = 'https://www.wandoujia.com/category/5019_940'
        for line in lines:
            pair = line.strip().split(",")
            url = pair[0]
            name = pair[1]
            logger.info("crawl {} url {}", name, url)
            category, url = self.crawl_one_row(url, refer_url)
            time.sleep(10)
            refer_url = url
            bank_category_writer.writerow([name, category, url])

    def crawl_one_row(self, url, refer_url):
        headers = {
            'cookie': 'ctoken=BEm2uU4VfssKzsrphcuTfG4E; sid=76237740163636877246432719076223; sid.sig=EwX6_Oxr7DHekS7GFY7P001ztLr94IVZtS-l1mUFRNw; _ga=GA1.2.1862676232.1636368773; UM_distinctid=17cff2df079999-06be8117331c58-1f3d6851-13c680-17cff2df07a98e; _bl_uid=09k9Ov7eqzbj0tpsbut2gw1v0t83; Hm_lvt_c680f6745efe87a8fabe78e376c4b5f9=1636368774; _gid=GA1.2.1359358233.1637113720; cna=IhN4GDCALjECAXPHbLe99tzP; xlly_s=1; CNZZDATA1272849134=436634356-1636359640-%7C1637137299; _uToken=T2gA9DyY1po5uRzztksBd_djRikyPJt72DxNXOuvcNfu0IC8QriCqEgh3yc_k90o_r4%3D; wdj_source=direct; _gat=1; Hm_lpvt_c680f6745efe87a8fabe78e376c4b5f9=1637148058; isg=BK2teQycsJg-cFVbyX_D-jR2vE8nCuHciuZn6--yWsSqZswYtFk1rXpwUTqAPvmU',
            'referer': refer_url,
            "user-agent": getheaders(),
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        response = requests.get(url, headers=headers, verify=False)
        tree = html.fromstring(response.text)
        categories = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[2]/a/text()')
        logger.info("categories {}", categories)
        privacy_url = tree.xpath('//a[@class=\'privacy-link\']/@href')
        logger.info("privacy_url {}", privacy_url)
        return ' '.join(categories), format_url(''.join(privacy_url))
