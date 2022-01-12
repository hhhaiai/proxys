import unittest
from spider.wandoujia_bank import WanDouJiaBankSpider
from spider.anzhi_bank import AnZhiBankSpider


class BankTestCase(unittest.TestCase):
    def test_bank(self):
        spider = WanDouJiaBankSpider()
        out_file = "/tmp/bank_category.csv"
        in_file = "/Users/xbkaishui/work/sources/wandoujia-spider/data/bank_list.txt"
        spider.crawl(in_file, out_file)

    def test_anzhi_bank(self):
        spider = AnZhiBankSpider()
        out_file = "/tmp/bank_category_anzhi.csv"
        in_file = "/Users/xbkaishui/work/sources/wandoujia-spider/data/anzhi.txt"
        spider.crawl(in_file, out_file)


if __name__ == '__main__':
    unittest.main()
