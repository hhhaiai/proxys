import json

import requests

from scrapy.selector import Selector

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

def handle_request(url,data=None,*args,**kwargs):
    resp = requests.get(url,headers=headers)
    return resp.text


def get_level1_url_list():
    # url = "https://www.wandoujia.com/category/app?pos=w/crumb/appcategory"
    url = "https://www.wandoujia.com/category/app"
    text = handle_request(url)
    sel = Selector(text=text)
    li_eles = sel.xpath("//ul[@class='clearfix tag-box']/li")
    level1_lsit = []
    for li in li_eles:
        level1_c_name = li.xpath("./a/text()").extract()[0]
        level1_c_url = li.xpath("./a/@href").extract()[0]
        level1_lsit.append({'name':level1_c_name,'url':level1_c_url})

    return level1_lsit


def get_level2_url_list(item):
    url = item['url']
    text = handle_request(url)
    sel = Selector(text=text)
    lis = sel.xpath("//ul[@class='switch-tab cate-tab']/li")
    id_list = []
    for li in lis[1:]:
        # levle2_name = li.xpath("./a/text()").extract()[0]
        levle2_url = li.xpath("./a/@href").extract()[0]
        id_str = levle2_url.split("/")[-1]
        catId = id_str.split("_")[0]
        subCatId = id_str.split("_")[1]
        id_list.append({'catId':catId,'subCatId':subCatId})
    return id_list


def parse_list(id_info,page=1):
    catId = id_info['catId']
    subCatId = id_info['subCatId']
    base_url = 'https://www.wandoujia.com/wdjweb/api/category/more?'
    params = {
        'catId':catId,
        'subCatId':subCatId,
        'page':page,
        'ctoken':'RqhzE2SB0qhNQDpW9JdWass3'
    }
    resp = requests.get(url=base_url,data=params)
    # print(catId,subCatId,page)
    # print(resp.request.url)
    resp_dict = json.loads(resp.text)
    data = resp_dict['data']
    per_page_app_url = []
    # 判断有内容再进行爬取
    if data['currPage'] != -1:
        content = data['content']
        sel = Selector(text=content)
        app_list = sel.xpath("//li")
        for app in app_list:
            # name = app.xpath(".//h2/a/text()").extract()[0]
            # desc = app.xpath(".//div[@class='comment']/text()").extract()[0] if app.xpath(".//div[@class='comment']/text()").extract()[0] else ""
            url = app.xpath(".//h2/a/@href").extract()[0]
            per_page_app_url.append(url)
        return per_page_app_url
    else:
        return []


def get_all_id():
    level1_list = get_level1_url_list()
    all_id_list = []
    # 获取所有的分类ID
    for item in level1_list:
        per_list = get_level2_url_list(item)
        all_id_list += per_list
    return all_id_list


def get_all_urls():
    all_id_list = get_all_id()
    # 获取每个分类的app 链接
    cat_urls = []
    for id_info in all_id_list:
        print("id_info",id_info)
        for p in range(1,2):
            per_page_urls = parse_list(id_info, page=p)
            cat_urls += per_page_urls
            break
    # print(len(all_urls))
    return cat_urls


def parse_detail(url):
    text = handle_request(url)
    sel = Selector(text=text)
    app_div = sel.xpath("//div[@class='app-info-wrap clearfix']")
    name = app_div.xpath(".//div[1]//span[@class='title']/text()").extract()[0]
    print(name)
    # 来源
    source_str = app_div.xpath(".//div[2]//i/@style").extract()
    if source_str:
        source = source_str[0].split(": ")[1][:2]
        print(source)
        a = 1






def parse_page_list():
    pass


if __name__ == '__main__':
    cat_urls = get_all_urls()
    for url in cat_urls:
        parse_detail(url)

