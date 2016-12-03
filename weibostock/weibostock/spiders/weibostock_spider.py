# coding=GBK
from scrapy.spiders import Spider
from scrapy import Request
from scrapy import FormRequest
from weibostock.items import InformationItem,TweetsItem
import weibostock.login as login
from scrapy.selector import Selector
import weibostock.info as info


class WeiboStockSpider(Spider):
    SZSHHK = info.SZSHHK
    SZSHHK_hasget = []
    name = "weibostock"
    domian = "http://weibo.cn"
    start_urls = []
    # 已经获取的微博ID
    Tweets_ID = []
    #已经访问的链接
    hasget_link = []
    cookies = []

    # 在这里进行登录，并获取登录后的URL，作为起始URL
    def __init__(self, *args, **kw):
        super(Spider, self).__init__(*args, **kw)
        weibo = login.WeiboLogin()
        loginurl = weibo.login()
        if loginurl:
            self.start_urls.append(loginurl)
            # 创建MozillaCookieJar实例对象
            self.cookies = weibo.getCookieInfo()
            print("self.cookies:", self.cookies)


    def parse(self, response):
        body = response.body.decode()
        print("response:",body)
        if body.find('feedBackUrlCallBack') != -1:
            #print response.body

            url = 'http://weibo.cn/'
            print("self.cookies:", self.cookies)

            # 查找关键词，利用下面路径，使用POST方法
            # 如果SHSZHK存在，则随机选择一个关键词进行搜索，搜索结束后去掉
            #print self.SZSHHK
            for everyone in self.SZSHHK:
                #SZSHHK_hasget = choice(self.SZSHHK)
                postdata = {
                    "keyword": everyone,
                    "smblog": u"搜微博"
                }
                yield FormRequest(url=info.searchUrl,
                                  formdata=postdata,
                                  callback=self.parseSearch,
                                  cookies=self.cookies)
        else:
            print('login failed: errno=%s, reason=%s')

    def parseSearch(self,response):
        #print response.body
        # 获取关注者微博信息
        # 将当前关注者的基本信息存入item中

        selector = Selector(response)
        Tweets = selector.xpath('//div[@class="c"]')
        if Tweets:
            # 跟parse1稍有不同，通过for循环寻找需要的对象
            for everytweet in Tweets:
                #排除微博为空
                if everytweet:
                    # 获取每条微博唯一id标识
                    m_id = everytweet.xpath('@id').extract()
                    if m_id:
                        mark_id = m_id[0]
                        if mark_id.find("M_") == -1 or not mark_id:
                            continue
                        # 当id不为空的时候加入到微博获取列表,去重操作，对于已经获取过的微博不再获取
                        if mark_id not in self.Tweets_ID:
                            tweetsItem = TweetsItem()
                            tweetsItem["_id"] = mark_id
                            print("mark_id:",mark_id)
                            contentTemp = everytweet.xpath('div[1]/span[@class="ctt"]')
                            content = contentTemp.xpath('string(.)').extract()

                            #在微博页面中，如果有图片的话，会分成两个div显示，第一个div会显示文字内容，第二个div显示图片和评论等内容
                            #如果没有图片的话，只会显示一个div，文字评论等都会在里面显示
                            mydiv = ""
                            if everytweet.xpath('div[2]').extract():
                                print("test temp:", everytweet.xpath('div[2]').extract())
                                mydiv = everytweet.xpath('div[2]')
                                timeloc = mydiv.xpath('span[@class="ct"]/text()').extract()
                                # picurl = everytweet.xpath('div[2]/a[2]/img/@src').extract()
                                picurl = mydiv.xpath('a[2]/@href').extract()
                                like = mydiv.xpath('a[3]/text()').extract()
                                transfer = mydiv.xpath('a[4]/text()').extract()
                                comment = mydiv.xpath('a[5]/text()').extract()
                            elif everytweet.xpath('div[1]').extract():
                                print("test temp:", everytweet.xpath('div[1]').extract())
                                mydiv = everytweet.xpath('div[1]')
                                timeloc = mydiv.xpath('span[@class="ct"]/text()').extract()
                                # picurl = everytweet.xpath('div[2]/a[2]/img/@src').extract()
                                picurl = "None"
                                like = mydiv.xpath('a[2]/text()').extract()
                                transfer = mydiv.xpath('a[3]/text()').extract()
                                comment = mydiv.xpath('a[4]/text()').extract()
                            else:
                                continue

                            if content:
                                print("content:", content)
                                tweetsItem['Content'] = content[0]
                            if picurl:
                                print(picurl)
                                tweetsItem['Pic_Url'] = picurl[0]
                            if comment:
                                print(comment)
                                # tweetsItem['Num_Comment'] = (comment[0])[(comment[0].index('[') + 1):comment[0].index(']')]
                                tweetsItem['Num_Comment'] = comment[0]
                            if like:
                                print(like)
                                # tweetsItem['Num_Like'] = (like[0])[(like[0].index('[') + 1):like[0].index(']')]
                                tweetsItem['Num_Like'] = like[0]
                            if transfer:
                                print(transfer)
                                # tweetsItem['NUm_Transfer'] = (transfer[0])[(transfer[0].index('[') + 1):transfer[0].index(']')]
                                tweetsItem['NUm_Transfer'] = transfer[0]
                            if timeloc:
                                tweetsItem['Time_Location'] = timeloc[0]
                            self.Tweets_ID.append(mark_id)
                            yield tweetsItem


        nextLink = selector.xpath('//div[@class="pa"]/form/div/a[1]/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            if nextLink not in self.hasget_link:
                nextLink = self.domian + nextLink
                print(nextLink)
                self.hasget_link.append(nextLink)
                yield Request(nextLink, callback=self.parseSearch, cookies=self.cookies)


