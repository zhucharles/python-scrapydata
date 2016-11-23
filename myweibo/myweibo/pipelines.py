# coding=GBK
from myweibo.items import TweetsItem,InformationItem
import MySQLdb

DEBUG = True

if DEBUG:
    username = 'root'
    pwd = '1029'
    database = 'weiboInfo'
    url = '127.0.0.1'
    port = '3306'


class MyweiboPipeline(object):
    #database connect
    def __init__(self):
        self.conn = MySQLdb.connect(user=username, passwd=pwd, db=database, host=url, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        # 清空表（测试阶段）：
        self.cursor.execute("truncate table TweetsInfo;")
        self.conn.commit()

    def process_item(self, item, spider):
        print "begin insert into database"
        try:
            if isinstance(item, TweetsItem):
                print "table info :",(item['_id'].encode('utf-8'),"  ",
                                      item['Content'].encode('utf-8'),"  ",
                                      item['Time_Location'].encode('utf-8'),"  ",
                                      item['Pic_Url'].encode('utf-8'),"  ",
                                      item['Num_Comment'].encode('utf-8'),"  ",
                                      item['Num_Like'].encode('utf-8'),"  ",
                                      item['NUm_Transfer'].encode('utf-8'))
                self.cursor.execute(
                    "insert into TweetsInfo(id,Content,Time_Location,Pic_Url,Num_Comment,Num_Like,NUm_Transfer) values(%s,%s,%s,%s,%s,%s,%s)",
                    (
                        item['_id'].encode('utf-8'),
                        item['Content'].encode('utf-8'),
                        item['Time_Location'].encode('utf-8'),
                        item['Pic_Url'].encode('utf-8'),
                        item['Num_Comment'].encode('utf-8'),
                        item['Num_Like'].encode('utf-8'),
                        item['NUm_Transfer'].encode('utf-8')
                    ))
                self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item

