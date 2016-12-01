from scrapy import cmdline

cmdline.execute("scrapy crawl weibostock -o items.json".split())