# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class MacbookjdItem(Item):
    _id = Field() #对应sku
    title = Field()
    img_url = Field()
    price = Field()
    description = Field()
    comments = Field()

class CommentItem(Item):
    _id = Field()
    start_num = Field()
    after_days = Field()
    time = Field()
    goods = Field()
    comment = Field()
    img_url = Field()
    like_num = Field()
    reply_num = Field()
    user = Field()
    level = Field()


