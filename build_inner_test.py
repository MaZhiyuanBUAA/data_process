#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
f=open('train.in')
f0=open('test_inner0.txt','w')
f1=open('test_inner1.txt','w')
f2=open('tragets.txt','w')
for i in range(10000):
  ele = f.readline()
  f0.write(ele)
  ele = ele.replace(' ','')
  f1.write(' '.join(jieba.cut(ele)))
  f2.write(f.readline())
f.close()
f1.close()
f0.close()
f2.close()

