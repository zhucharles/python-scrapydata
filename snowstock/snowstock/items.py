from scrapy import Item,Field


"""
    用于雪球爬虫下评论内容
"""
class SnowstockInfoItem(Item):
    user_name = Field() #对应的实际上是userTitle
    title = Field() #这个是不同于微博的地方，每个评论都有标题，获取可以从标题提取该文的情感倾向-------这个对应的实际上是h4，但不是每个帖子都有
    content = Field() #这个对应的是正文，summary以及detail，其中detail可能有可能没有
    time = Field() #对应的是meta下面的time信息
    location = Field() #对应的是meta下面的span，来自...
    transfer_num = Field() #转发数，对应的是meta下面的ops
    keep_num = Field() #收藏数，对应的是meta下面的ops
    reward_num = Field() #打赏数，对应的是meta下面的ops
    comment_num = Field() #评论数，对应的是meta下面的ops
