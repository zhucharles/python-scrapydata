# coding=GBK
from scrapy import Item,Field

#follow person information
class InformationItem(Item):
    _id = Field()
    Info = Field()
    Num_Tweets = Field()
    Num_Follows = Field()
    Num_Fans = Field()
    Home_Page = Field()

#tweets info
class TweetsItem(Item):
    _id = Field()
    Content = Field()
    Time_Location = Field()
    Pic_Url = Field()
    Num_Comment = Field()
    Num_Like = Field()
    NUm_Transfer = Field()