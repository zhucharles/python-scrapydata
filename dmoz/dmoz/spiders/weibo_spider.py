# coding=GBK
import scrapy
from scrapy.spider import Spider
from dmoz.items import InformationItem,TweetsItem
from scrapy.selector import Selector
from scrapy.http import Request

class WeiboSpider(Spider):
    name = "dmoz"
    #这里可以多写几个用户，目前用的是我自己的账户
    start_url = ["http://weibo.cn/3745970722/follow"]
    url = "http://weibo.cn"
    # 记录待爬的微博ID
    scrawl_ID = set(start_url)
    #已经获取的用户ID存入列表中
    Follow_ID = []
    #已经获取的微博ID
    Tweets_ID = []

    #最开始的爬虫
    def start_requests(self):
        while True:
            ID = self.scrawl_ID.pop()
            self.Follow_ID.append(ID)  # 加入已爬队列
            ID = str(ID)
            follows = []
            followsItems = InformationItem()
            #followsItems["_id"] = ID
            #followsItems["follows"] = follows
            url_information0 = "http://weibo.cn/attgroup/opening?uid=%s" % ID
            url_follows = "http://weibo.cn/%s/follow" % ID
            url_tweets = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
            yield Request(url=url_follows, meta={"item": followsItems, "result": follows},
                          callback=self.parseForFollow)  # 去爬关注人
            yield Request(url=url_information0, meta={"ID": ID}, callback=self.parse)  # 去爬个人信息
            yield Request(url=url_tweets, meta={"ID": ID}, callback=self.parseForCorrect)  # 去爬微博

    #解析函数，用于解析爬下来的网页,是下载器的回调函数，当request请求过后，返回response响应并调用此函数
    def parse(self,response):
        #数据存放的对象
        infoItem = InformationItem()
        tweetsItem = TweetsItem()
        #选择器，用于获取网页中的标签元素和值,response入参，后面直接使用selector
        selector = Selector(response)
        print(selector)

        #关注人列表，不知道为什么需要这样，暂时先用这个
        Followlist = selector.xpath('//tr/td[2]/a[2]/@href').extract()
        print "关注的数量:",len(Followlist)

        #对于每个关注人而言
        for everyone in Followlist:
            #获取每个关注人url中有关用户ID的部分
            followId = everyone[(everyone.index("uid")+4):(everyone.index("rl")-1)]
            #关注人的主页， 其中用户ID由上面给出
            followUrl = "http://weibo.cn/%s/profile" % followId
            print "关注人ID:",followId,"------关注人的主页:",followUrl
            #获取我所需要的信息，这里是获取原创带图且最近一年内的微博，具体参数可通过F12从request中获知
            correctUrl = "http://weibo.cn/%s/profile?hasori=1&haspic=1&starttime=20151120&endtime=20161120&advancedfilter=1&page=1" % followId

            if followId not in self.Follow_ID:
                # 对每个获取的关注人ID重新进行爬虫--我的天那，如果关注的人很多，这且不是要无穷无尽
                #重新发送request请求，传入一些参数，并调用回调函数,meta主要用于存放请求的一些信息
                yield Request(url=followUrl,meta={"item":infoItem, "ID": followId, "URL": followUrl},callback=self.parseForFollow)
                #对当前获取的关注人拥有的微博进行爬数据，这个我还是每个爬一点算了，不然太多了
                yield Request(url=correctUrl,meta={"item":tweetsItem,"ID":followId},callback=self.parseForCorrect)
                self.Follow_ID.append(followId)

            # 判断是否有下一页，如果有下一页，使用request进行请求，调用当前函数为回调函数，有点类似递归
        nextUrl = selector.xpath("//div[@class='pa']/form/div/a/@href").extract()
        if nextUrl:
            yield Request(url=self.url + nextUrl, callback=self.parse)
        else:
            print self.Follow_ID

    #处理获取到的关注者主页
    def parseForFollow(self,response):
        #将当前关注者的基本信息存入item中
        infoItem = response.meta['item']
        infoItem['_id'] = response.meta['ID']
        infoItem['Home_Page'] = response.meta['URL']

        selector = Selector(response)
        info = selector.xpath("//div[@class='ut']/span[@class='ctt']/text()").extract()
        #join 返回通过指定字符连接序列中元素后生成的新字符串
        newInfo = '/'.join(info)
        try:
            # exceptions.TypeError: expected string or buffer ??
            infoItem['Info'] = newInfo
        except:
            pass

        #tip2中各信息,Num_Tweet Num_Follows Num_Fans
        num_tweets = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/span/text()').extract()  # 微博数
        num_follows = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/a[1]/text()').extract()  # 关注数
        num_fans = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/a[2]/text()').extract()  # 粉丝数
        #获取[ ]之间的数据
        if num_tweets:
            #之所以带[0]是因为怕有相同的标签
            infoItem['Num_Tweets'] = (num_tweets[0])[(num_tweets[0].index('[')+1):num_tweets[0].index(']')]
        if num_follows:
            infoItem['Num_Follows'] = (num_follows[0])[(num_follows[0].index('[') + 1):num_follows[0].index(']')]
        if num_fans:
            infoItem['Num_Fans'] = (num_fans[0])[(num_fans[0].index('[') + 1):num_fans[0].index(']')]
        yield infoItem



    #获取关注者微博信息
    def parseForCorrect(self,response):
        # 将当前关注者的基本信息存入item中
        tweetsItem = response.meta["Item"]
        tweetsItem["_id"] = response.meta["ID"]

        selector = Selector(response)
        Tweets = selector.xpath('//div[@class="c"]')
        # 跟parse1稍有不同，通过for循环寻找需要的对象
        for everytweet in Tweets:
            # 获取每条微博唯一id标识
            mark_id = everytweet.xpath('@id').extract()
            print mark_id
            # 当id不为空的时候加入到微博获取列表,去重操作，对于已经获取过的微博不再获取
            if mark_id and mark_id not in self.TweetsID:
                content = everytweet.xpath('div/span[@class="ctt"]/text()').extract()
                timeloc = everytweet.xpath('div[2]/span[@class="ct"]/text()').extract()
                picurl = everytweet.xpath('div[2]/a[2]/img/@src').extract()
                like = everytweet.xpath('div[2]/a[3]/text()').extract()
                transfer = everytweet.xpath('div[2]/a[4]/text()').extract()
                comment = everytweet.xpath('div[2]/a[5]/text()').extract()
                if content:
                    tweetsItem['Content'] = content[0]
                if picurl:
                    tweetsItem['Pic_Url'] = picurl[0]
                if comment:
                    tweetsItem['Num_Comment'] = (comment[0])[(comment[0].index('[')+1),comment[0].index(']')]
                if like:
                    tweetsItem['Num_Like'] = (like[0])[(like[0].index('[') + 1), like[0].index(']')]
                if transfer:
                    tweetsItem['NUm_Transfer'] = (transfer[0])[(transfer[0].index('[') + 1), transfer[0].index(']')]

        nextLink = selector.xpath('//div[@class="pa"]/form/div/a/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(self.url+nextLink, callback=self.parseForCorrect)






















