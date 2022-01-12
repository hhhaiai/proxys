# wandoujia

基于[AlmostProgramer/wandoujia](https://github.com/AlmostProgramer/wandoujia)

做了如下修改：

1、下载了应用

2、在Requeset请求中增加优先级，以避免爬取新网页远多于下载应用的情况

由于scrapy默认不会对同一个url爬取两次，因此没有考虑对保存在数据库里的数据去重。


