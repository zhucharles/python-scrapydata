# coding=GBK
import xlrd
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
#读取情感本体词汇中的词语
data = xlrd.open_workbook(u"./ontologydata/word_emotion_ontology.xlsx")
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
print("一共有:",nrows,"行---",ncols,"列")


mydata = []

#循环行列表数据
for i in range(nrows):
    tempdata = [(table.row_values(i)[0]).encode("utf8"),(table.row_values(i)[4]).encode("utf-8")]
    #tempdata.append(table.row_values(i)[0])
    #tempdata.append(table.row_values(i)[4])
    mydata.append(tempdata)
    print("情感为：",(tempdata[0]).decode("utf8"),"----所属类别为：",(tempdata[1]).decode("utf8"))