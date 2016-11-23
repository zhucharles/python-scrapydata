import scrapy
from dmoz.items import DmozItem
#spider file
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    #parse function

    def parse(self, response):
        #-2 is python
        #response has attribute url,we can see the attribute through F12
        # filename = response.url.split("/")[-2]
        # with open(filename,"wb")as f:
        #     f.write(response.body)


        ulli = response.xpath("//ul/li")
        for sel in ulli:
            # item
            item = DmozItem()
            item["title"] = sel.xpath("a/text()").extract()
            item["link"] = sel.xpath("a/@href").extract()
            item['description'] = sel.xpath('text()').extract()
            yield item




