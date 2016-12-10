from scrapy import Item,Field


"""
    用于雪球爬虫下评论内容
"""
class SnowstockInfoItem(Item):
    symbol = Field() #所属的股票
    user_id = Field() #对应的实际上是user_id
    user = Field #这里是一个对象，对应的是user，用户的属性
    title = Field() #这个是不同于微博的地方，每个评论都有标题，获取可以从标题提取该文的情感倾向-------这个对应的实际上是json中的title，但不是每个帖子都有
    description = Field() #这个对应的是正文，summary以及detail，其中detail可能有可能没有
    created_at = Field() #对应的是meta下面的created_at信息，创建的时间，这里是时间戳，但是可以根据这个来排序，注意，这里实际上后面多加了三个0
    edited_at = Field() #修改的时间，这里是时间戳，但是可以根据这个来排序，注意，这里实际上后面多加了三个0
    timeBefore = Field() #"11-27 19:14" 这个跟create_at有什么没区别？？
    pic = Field() #图片地址
    source = Field() #对应的是meta下面的span，来自...  对应的应该是json中的source
    retweet_count = Field() #转发数，对应的是meta下面的ops
    fav_count = Field() #收藏数，对应的是meta下面的ops
    reward_count = Field() #打赏数，对应的是meta下面的ops
    reply_count = Field() #评论数，对应的是meta下面的ops




