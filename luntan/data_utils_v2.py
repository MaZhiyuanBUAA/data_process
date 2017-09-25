#coding:utf-8
#author:MaZhiyuan
#objective:Luntan data processeing

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import re
import jieba
import time
from collections import defaultdict
class config():
  def __init__(self):
    self.data_path = '/home/zyma/work/ruisheng.final'
    self.minganci_path = 'minganci.txt'
    self.search_rules = [u'[1-9]\d{4,}','\.com|\.cn|\.top|\.org|http|html|www|\.exe']
    self.sub_rules = [(u'\r|\n|\f',''),(u'^[,.:;?!，。、？：；！]+',''),
                 (u'[^\u4e00-\u9fa5,.:;\'"?!，。、？：；·“”‘’！《》a-zA-Z\s\d]','')]
    self.save2 = 'ruisheng.json'
    self.range_post = (2,15)
    self.range_resp = (2,20)
    self.display_step = 100000
    self.num_reserved = 3

class process():
  def __init__(self,data_path,
               minganci_path,
               search_rules,
               sub_rules,
               save2='results.json'):
    
    self.data_path = data_path
    self.minganci_path = minganci_path
    self.save2 = save2
    self.search_rules = search_rules
    self.sub_rules = sub_rules
    assert type(search_rules) is list
    assert type(sub_rules) is list
    print('下载敏感词库:%s'%self.minganci_path)
    with open(self.minganci_path) as f:
      self.minganci = [ele.strip().decode('utf-8') for ele in f.readlines()]

  def minganci_filter(self,sentence):
    for w in self.minganci:
      if sentence.find(w)>=0:
        return True
    return False

  def length_filter(self,sentence,length_range=(2,15)):
    #sentence has been cut by jieba
    l = len(sentence.split())
    if l>=length_range[0] and l<=length_range[1]:
      return True
    else:
      return False

  def regular_filter(self,sentence):
    for rule in self.search_rules:
      if re.search(rule,sentence):
        return True
    return False

  def regular_sub(self,sentence):
    #sub_rules=[(replace,replaceby)]
    for rule in self.sub_rules:
       sentence = re.sub(rule[0],rule[1],sentence)
    return sentence
  def main(self,range_post,range_resp,num_reserved,display_step):
    startTime = time.time()
    num_processed = 1
    num_query = 0
    f = open('test.txt','w')
    with open(self.data_path) as data_f:
      with open(self.save2,'w') as save_f:
        item = data_f.readline()
        while item:
          if num_processed%display_step == 0:
            mean_time = (time.time()-startTime)*display_step/num_processed
            print('%d lines have been processed,time per %d line %f,query cleared %d'%(num_processed,display_step,mean_time,num_query))
          num_processed += 1
          item_saved = {}
          item = json.loads(item)
          post = self.regular_sub(item['post']).strip()
          if self.minganci_filter(post):
            item = data_f.readline()
            continue
          if self.regular_filter(post):
            item = data_f.readline()
            continue
          post = ' '.join([ele.strip() for ele in jieba.cut(post) if ele.strip()])
          if self.length_filter(post,range_post):
            item_saved['post'] = post
          else:
            item = data_f.readline()
            continue
          item_saved['cmnt'] = []
          num_cmnt = 0
          for cmnt in item['cmnt']:
            content = cmnt['content'].decode('utf-8')
            uid = cmnt['userID']
            content = self.regular_sub(content).strip()
            if self.minganci_filter(content):
              continue
            if self.regular_filter(content):
              continue
            content = ' '.join([ele.strip() for ele in jieba.cut(content) if ele.strip()])
            if self.length_filter(content,range_resp):
              cmnt_saved = {'content':content,'userID':uid}
              item_saved['cmnt'].append(cmnt_saved)
              f.write('Q:'+post.encode('utf-8')+'\n'+'A:'+content.encode('utf-8')+'\n')
              num_cmnt += 1
            else:
              continue
            if num_cmnt >= num_reserved-1:
              break
          item_saved['url'] = item['url']
          if item_saved['cmnt']:
            #print(item_saved['post'].encode('utf-8'))
            item_saved = json.dumps(item_saved)
            save_f.write(item_saved+'\n')
            num_query += 1
          item = data_f.readline()
    f.close()
def processMinganciAdded(path):
  f = open('minganci_added.txt')
  minganci_added =[ele.strip().decode('utf-8') for ele in  f.readlines()]
  f.close()
  def with_minganci(sentence):
    for ele in minganci_added:
      if sentence.find(ele)>-1:
        return True
    return False
  with open(path) as f,open(path+'.update','w') as rf:
    s = f.readline()
    n = 1
    ST = time.time()
    while s:
      s = json.loads(s)
      post = s['post']
      if n%100000 == 0:
        print('line %d,time per %d:%f'%(n,100000,(time.time()-ST)/n*100000))
      if with_minganci(post):
        s = f.readline()
        n += 1
        continue
      else:
        item = {}
        item['post'] = post
        item['url'] = s['url']
        item['cmnt'] = []
        for ele in s['cmnt']:
          if with_minganci(ele['content']):
            continue
          item['cmnt'].append(ele)
        if item['cmnt']:
          rf.write(json.dumps(item)+'\n')
        s = f.readline()
        n += 1
if __name__ == '__main__':
  #conf = config()
  #processor = process(conf.data_path,conf.minganci_path,conf.search_rules,conf.sub_rules,conf.save2)
  #processor.main(conf.range_post,conf.range_resp,conf.num_reserved,conf.display_step)     
  processMinganciAdded('ruisheng.json')     
