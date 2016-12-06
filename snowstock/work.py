from scrapy import cmdline

cmdline.execute("scrapy crawl snowstock -o items.json".split())
