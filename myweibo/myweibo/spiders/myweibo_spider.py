# coding=GBK
from  scrapy.spiders import Spider
import myweibo.login as login
from scrapy.selector import Selector
import json,re
import scrapy
from scrapy import Request
from myweibo.items import InformationItem,TweetsItem
import cookielib

class MyWeiboSpider(Spider):
    name = "myweibo"
    domian = "http://weibo.cn/"
    login_urls = []
    start_urls = []
    old_weibos = []
    #已经获取的用户ID存入列表中
    Follow_ID = []
    #已经获取的微博ID
    Tweets_ID = []
    cookies = []

    #在这里进行登录，并获取登录后的URL，作为起始URL
    def __init__(self,*args,**kw):
        super(Spider,self).__init__(*args,**kw)
        weibo = login.WeiboLogin()
        loginurl = weibo.login()
        if loginurl:
            #starturl = "http://weibo.com"
            self.start_urls.append(loginurl)
            # 创建MozillaCookieJar实例对象
            self.cookies = weibo.getCookieInfo()
            print "self.cookies:", self.cookies
                # cookie = "<Cookie ALC=ac%3D2%26bt%3D1479746756%26cv%3D5.0%26et%3D1511282756%26scf%3D%26uid%3D3815666512%26vf%3D0%26vs%3D0%26vt%3D0%26es%3De5f0cbff8d7d1a43b7d312af20e03fad for .login.sina.com.cn/>, <Cookie LT=1479746756 for .login.sina.com.cn/>, <Cookie tgc=TGT-MzgxNTY2NjUxMg==-1479746756-ja-4002E565EEDFBCD528E34BA900197741 for .login.sina.com.cn/>, <Cookie ALF=1511282756 for .sina.com.cn/>, <Cookie SCF=AljccvcU-MXu7dAv8tAU2PqxO4Mh7up-usmKN5WrBDF0xOM-PlP46wE8x9D412lFm5WyaEIPSrPOOaWwny-SjJY. for .sina.com.cn/>, <Cookie SUB=_2A251N1SUDeTxGeVG6lcX9ijJyj6IHXVWRcFcrDV_PUNbm9ANLU3fkW8TgsgYNcJIhGs7MK3rk72XiOEqaw.. for .sina.com.cn/>, <Cookie SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Haujr-W3aFpl1sG5HoUay5NHD95Q01h2fSoqcSK2EWs4Dqcjdi--Xi-iWiK.pi--NiKLsi-z0i--ci-zpiKnN for .sina.com.cn/>, <Cookie sso_info=v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLOOg4S1jaOYto2ThLKJp5WpmYO0s46DhLWNo5i2jZOEsg== for .sina.com.cn/>"
                # p = re.compile('\<LWPCookieJar\[\<Cookie (.*?) for .weibo.com\/\>\]\>')
                # cookiess = re.findall(p, cookie)
                # cookiess = (cookiejar.split('=') for cookiejar in cookiess)
                # print "cookies:",cookiess
                # for each in dict(cookiess):
                #     print "each:",each
                #self.cookies = dict(cookie)
                # with open(self.cookie_file, 'wb+') as f:
            #     for cookie in cookie_jar:
            #         f.write(str(cookie) + '\n')

    def parse(self, response):
        #print "response:",response.body
        if response.body.find('feedBackUrlCallBack') != -1:
            print response.body
            url = 'http://weibo.cn/'
            print "self.cookies:",self.cookies
            yield Request(url=url, callback=self.parseFollow,cookies=self.cookies)
        else:
            print('login failed: errno=%s, reason=%s')

    # def start_requests(self):
    #     url = 'http://weibo.com/u/3815666512/home?wvr=5'
    #     yield Request(url=url, callback=self.parseFollow)


    def parseFollow(self,response):
        #print response.body
        selector = Selector(response)
        #followUrl = selector.xpath("//div[@class='WB_innerwrap']/ul/li[1]/a/@href").extract()

        followurl = selector.xpath("//div[@class='u']/div[@class='tip2']/a[2]/@href").extract()
        if followurl:
            follow = followurl[0]
            print "followUrl:",follow
            #domian = "http://weibo.cn/"
            yield Request(url=self.domian+follow, callback=self.parsePerson)


    # 解析函数，用于解析爬下来的网页,是下载器的回调函数，当request请求过后，返回response响应并调用此函数
    def parsePerson(self, response):
        # 数据存放的对象
        infoItem = InformationItem()
        tweetsItem = TweetsItem()
        # 选择器，用于获取网页中的标签元素和值,response入参，后面直接使用selector
        selector = Selector(response)

        # 关注人列表，不知道为什么需要这样，暂时先用这个
        # http://weibo.cn/attention/remark?uid=1781379945&rl=1&vt=4
        Followlist = selector.xpath('//tr/td[2]/a[2]/@href').extract()

        if len(Followlist)>0:
            print "follow numbers:", len(Followlist)
            # 对于每个关注人而言
            for everyone in Followlist:
                # 获取每个关注人url中有关用户ID的部分
                followId = everyone[(everyone.index("uid") + 4):(everyone.index("rl") - 1)]
                print "followId:",followId

                # 关注人的主页， 其中用户ID由上面给出
                followUrl = "http://weibo.cn/%s/profile" % followId
                print "followId:", followId, "------followUrl:", followUrl
                # 获取我所需要的信息，这里是获取原创带图且最近一年内的微博，具体参数可通过F12从request中获知
                correctUrl = "http://weibo.cn/%s/profile?hasori=1&haspic=1&starttime=20161020&endtime=20161120&advancedfilter=1&page=1" % followId

                if followId not in self.Follow_ID:
                    # 对每个获取的关注人ID重新进行爬虫--我的天那，如果关注的人很多，这且不是要无穷无尽
                    # 重新发送request请求，传入一些参数，并调用回调函数,meta主要用于存放请求的一些信息
                    yield Request(url=followUrl, meta={"item": infoItem, "ID": followId, "URL": followUrl},
                                  callback=self.parseForFollow)
                    # 对当前获取的关注人拥有的微博进行爬数据，这个我还是每个爬一点算了，不然太多了
                    yield Request(url=correctUrl, meta={"item": tweetsItem, "ID": followId},
                                  callback=self.parseForCorrect)
                    self.Follow_ID.append(followId)

                # 判断是否有下一页，如果有下一页，使用request进行请求，调用当前函数为回调函数，有点类似递归
        nextUrl = selector.xpath("//div[@class='pa']/form/div/a/@href").extract()
        if nextUrl:
            nextUrl = nextUrl[0]
            yield Request(url=self.domian + nextUrl, callback=self.parsePerson)

    # 处理获取到的关注者主页
    def parseForFollow(self, response):
        # 将当前关注者的基本信息存入item中
        infoItem = response.meta['item']
        infoItem['_id'] = response.meta['ID']
        infoItem['Home_Page'] = response.meta['URL']

        selector = Selector(response)
        info = selector.xpath("//div[@class='ut']/span[@class='ctt']/text()").extract()
        # join 返回通过指定字符连接序列中元素后生成的新字符串
        newInfo = '/'.join(info)
        try:
            # exceptions.TypeError: expected string or buffer ??
            infoItem['Info'] = newInfo
        except:
            pass

        # tip2中各信息,Num_Tweet Num_Follows Num_Fans
        num_tweets = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/span/text()').extract()  # 微博数
        num_follows = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/a[1]/text()').extract()  # 关注数
        num_fans = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/a[2]/text()').extract()  # 粉丝数
        # 获取[ ]之间的数据
        if num_tweets:
            # 之所以带[0]是因为怕有相同的标签
            infoItem['Num_Tweets'] = (num_tweets[0])[(num_tweets[0].index('[') + 1):num_tweets[0].index(']')]
        if num_follows:
            infoItem['Num_Follows'] = (num_follows[0])[(num_follows[0].index('[') + 1):num_follows[0].index(']')]
        if num_fans:
            infoItem['Num_Fans'] = (num_fans[0])[(num_fans[0].index('[') + 1):num_fans[0].index(']')]
        yield infoItem



    # 获取关注者微博信息
    def parseForCorrect(self, response):
        # 将当前关注者的基本信息存入item中
        tweetsItem = response.meta["item"]
        tweetsItem["_id"] = response.meta["ID"]

        selector = Selector(response)
        Tweets = selector.xpath('//div[@class="c"]')
        if Tweets:
            # 跟parse1稍有不同，通过for循环寻找需要的对象
            for everytweet in Tweets:
                # 获取每条微博唯一id标识
                mark_id = everytweet.xpath('@id').extract()
                print mark_id
                # 当id不为空的时候加入到微博获取列表,去重操作，对于已经获取过的微博不再获取
                if mark_id and mark_id not in self.Tweets_ID:
                    content = everytweet.xpath('div/span[@class="ctt"]/text()').extract()
                    timeloc = everytweet.xpath('div[2]/span[@class="ct"]/text()').extract()
                    #picurl = everytweet.xpath('div[2]/a[2]/img/@src').extract()
                    picurl = everytweet.xpath('div[2]/a[2]/@href').extract()
                    like = everytweet.xpath('div[2]/a[3]/text()').extract()
                    transfer = everytweet.xpath('div[2]/a[4]/text()').extract()
                    comment = everytweet.xpath('div[2]/a[5]/text()').extract()
                    if content:
                        #print content
                        tweetsItem['Content'] = content[0]
                    if picurl:
                        #print picurl
                        tweetsItem['Pic_Url'] = picurl[0]
                    if comment:
                        #print comment
                        #tweetsItem['Num_Comment'] = (comment[0])[(comment[0].index('[') + 1):comment[0].index(']')]
                        tweetsItem['Num_Comment'] = comment[0]
                    if like:
                        #print like
                        #tweetsItem['Num_Like'] = (like[0])[(like[0].index('[') + 1):like[0].index(']')]
                        tweetsItem['Num_Like'] = like[0]
                    if transfer:
                        #print transfer
                        #tweetsItem['NUm_Transfer'] = (transfer[0])[(transfer[0].index('[') + 1):transfer[0].index(']')]
                        tweetsItem['NUm_Transfer'] = transfer[0]
                    if timeloc:
                        tweetsItem['Time_Location'] = timeloc[0]


        yield tweetsItem
        nextLink = selector.xpath('//div[@class="pa"]/form/div/a/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(self.domian + nextLink, callback=self.parseForCorrect,meta={"item":tweetsItem,"ID":tweetsItem["_id"]})


