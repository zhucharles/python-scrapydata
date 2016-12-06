# coding=utf8
from scrapy.spiders import Spider
from scrapy.selector import Selector
"""
    现在来真正爬去雪球页面
    格力电器：https://xueqiu.com/S/SZ000651
"""
class SnowStockSpider(Spider):
    name = "snowstock"
    start_urls = ["https://xueqiu.com/S/SZ000651"] #格力电器

    #先尝试爬格力电器页面的评论算了，然后按时间进行排列看有多少个评论
    def parse(self, response):
        selector = Selector(response)
        ullist = selector.xpath("//div[@id='statusList']/ul[@class='status-list']").extract()
        if ullist:
            print(ullist)

