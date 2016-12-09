# coding=gbk
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import time
import json
"""
    现在来真正爬去雪球页面
    格力电器：https://xueqiu.com/S/SZ000651
"""
class SnowStockSpider(Spider):
    name = "snowstock"
    #start_urls = ["https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=01918&hl=0&source=all&sort=alpha&page=5&_=1481013713658"] #格力电器
    start_urls = "https://xueqiu.com/S/"
    stock_ids = ["SZ000651"] #可能以后爬取多个股票id

    #先尝试爬格力电器页面的评论算了，然后按时间进行排列看有多少个评论
    """
        对下一个评论页面：
        https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=01918&hl=0&source=all&sort=alpha&page=5&_=1481013713658
        返回的是一个json，就是评论的内容，能否只请求这个json呢？
        参数有：count、comment、symbol、hl、source、sort、page、_
        count为每页的帖子数量
        comment未知
        symbol为股票ID
        hl未知
        source未知
        sort为排序方式，time表示按时间排序，alpha表示按帖子热度排序
        page为页面数
        _为时间戳
    """
    cookies={
        "bid":"245d7b1e72c5afb4f22e2709275454ac_iwbw50ic",
        "s":"8s19kxfky4", #这个值在浏览器中是动态变化的，但是设置为固定仍然成功了，这个问题没有解决！
        "snbim_minify":"True",
        "xq_a_token":"47697ade308c557aab035d60928e25f3e4dea8f6",
        "xq_r_token":"c802a9a38f3d779d8181f536020f1da0e6a6c2e5"
    }

    def start_requests(self):
        for id in self.stock_ids:
            url = self.start_urls + id
            yield Request(url,meta={"stock_id":id},callback=self.parse)


    def parse(self, response):
        count = 10
        comment = 0
        symbol = response.meta["stock_id"]
        hl = 0
        source = "all"
        sort = "time"
        pages = range(100,1)
        page = 1
        current_time = time.time() #获取当前时间戳
        #成功了，需要添加上面的参数，具体解释见上部
        parse_url = "https://xueqiu.com/statuses/search.json?count={0}&comment={1}&symbol={2}&hl={3}&source={4}&sort={5}&page={6}&_={7}".format(
                            count,comment,symbol,hl,source,sort,page,current_time) #格力电器
        print("MyCookie",self.cookies)
        print("访问的url:",parse_url)
        yield Request(parse_url,cookies=self.cookies,dont_filter=True,callback=self.parse_page)



    def parse_page(self,response):
        postings = response.body.decode()
        print(postings)
        #postdict = dict(postings)

        postjson =  json.loads(postings)
        print(postjson)




