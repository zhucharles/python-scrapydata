# coding=GBK
import MySQLdb
from macbookJD.items import MacbookjdItem,CommentItem

DEBUG = True

if DEBUG:
    dbuser = 'root'
    dbpass = '1029'
    dbname = 'macbookInfo'
    dbhost = '127.0.0.1'
    dbport = '3306'

class MacbookjdPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        # 建立需要存储数据的表
        # 清空表（测试阶段）：
        self.cursor.execute("truncate table MacbookjdInfo;")
        self.conn.commit()

    def process_item(self, item, spider):
        # curTime = datetime.datetime.now()
        print("begin insert info into databse")
        if isinstance(item, MacbookjdItem):
            print "begin insert info into databse"
            try:
                print "item['id']:",item['_id']
                print "item['title']:",item['title']
                print "item['img_url']:",item['img_url']
                self.cursor.execute("""insert into MacbookjdInfo (id, title, img_url, price, description, comments)
                                            values (%s, %s, %s, %s, %s, %s)""",(
                    item['_id'].encode('utf-8'),
                    item['title'].encode('utf-8'),
                    item['img_url'].encode('utf-8'),
                    item['bo'].encode('utf-8'),
                    " ",
                    #item['description'].encode('utf-8'),
                    item['comments'].encode('utf-8'),))
                self.conn.commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])

        return item
