#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import re
import jieba
from collections import defaultdict

def json2txt(path):
  #jsonfile:{"post":"xxxx","cnmt":[{"content":"xxxx"},{"content":"xxxxx"}]}
  f = open(path)
  result_f = open(path+'.processed','w')
  line = f.readline()
  existed = set()
  n0,n1,num_adv = 0,0,0
  def _clear(s):
    #comment = re.sub(u'^<.*>|^【.*】|^#.*#|\u200b','',s.decode('utf-8'))
    comment = s.decode('utf-8').strip()
    #filter place info
    #comment = re.sub(u'我在:2.+$|2.+$','',comment)
    #comment = re.sub(u'O网页链接|O[\u4e00-\u9fa5]+$','',comment)
    #filter "展开全文c"
    #comment = re.sub(u'展开全文c$','',comment)
    #punct duplicate remov
    #comment = re.sub(u'!+','!',comment)
    #comment = re.sub(u'！+','！',comment)
    #comment = re.sub(u'。+','。',comment)
    #comment = re.sub(u'，+','，',comment)
    #comment = re.sub(u',+',',',comment)
    comment = re.sub(u'^[,.:;?!，。、？：；！]+','',comment)
    return re.sub(u',+',',',comment)
  def good_sentence(post):
    if (not re.findall(u'[\u4e00-\u9fa5]',post)) or (re.findall(u'照片|图片|配图|链接|视频|展开全文',post)) or re.findall('[1-9]\d{4,}',post):
      return False
    else:
      return True
 
  while line:
    n0 += 1
    line = json.loads(line)
    post = line["post"]
    #print(post)
    comments = line["cmnt"]
    comments = [re.sub(u'\n|\r|\f','',ele['content']) for ele in comments]
    post = _clear(post)
    #post = re.sub(u'^@\S+','',post)
    post = re.sub(u'\n|\r|\f','',post)
    if (post in existed) or (not good_sentence(post)):
      #print(post)
      #print('ok000')
      line = f.readline()
      continue
    else:
      comment = None
      comments_dict = defaultdict(int)
      for ele in comments:
        comments_dict[ele] += 1
      memory = 0
      for ele in comments_dict.keys():
        #ad remove
        if comments_dict[ele]>1 or ele.find('@')>=0 or (not good_sentence(ele)):
          num_adv += 1
          #if num_adv%100==0:
          #  print(len(comments))
          continue
        #@other
        else:
          comment = _clear(ele)
          #comment = re.sub(u'\n|\r|\f','',comment)
          #if re.findall(u'[\u4e00-\u9fa5]',comment):
          if comment:
            existed.add(post)
            written = post.strip()+'\n'+comment.strip()+'\n'
            result_f.write(written.encode('utf-8'))
            memory += 1
            if memory>2:
              break
      line = f.readline()
  f.close()
  result_f.close()
  print((n0,n1,num_adv))

def duplicate_remv(path):
  #textfile
  f = open(path)
  result_f = open(path+'.processed','w')
  negetiv_f = open(path+'.neg','w')
  post, resp = f.readline(), f.readline()
  existed = set()
  while post and resp:
    line_ = re.sub('\s','',post)+re.sub('[^\S]','',resp)
    if line_ in existed:
      pass
    else:
      existed.add(line_)
      lpo = len(post.split())
      lre = len(resp.split())
      if lpo<=15 and lre<=20:
        result_f.write(post+resp)
      else:
        negetiv_f.write(post+resp)
        pass
    post, resp = f.readline(), f.readline()
  f.close()
  result_f.close()
  negetiv_f.close()

def weibo(path):
  f = open(path)
  result_f = open(path+'.processed','w')
  query,resp = f.readline(),f.readline()
  #existed = set()
  i0,i1 = 0,0
  #useless_words = '|'.join([u'评论配图',u'秒拍视频'])
  
  #def _useless(s):
  #  return re.sub(useless_words,'',s)
  while query and resp:
    i0 += 1
    query = query.decode('utf-8').strip()
    resp = resp.decode('utf-8').strip()

    #query =_useless(query)
    #resp = _useless(resp)
    query_cutted = jieba.cut(query)
    resp_cutted = jieba.cut(resp)
    
    query_cutted = [ele for ele in query_cutted if ele.strip()]
    resp_cutted = [ele for ele in resp_cutted if ele.strip()]

    lqu,lre = len(query_cutted),len(resp_cutted)
    
    query_cutted = ' '.join(query_cutted)
    resp_cutted = ' '.join(resp_cutted)
    #remove duplicate
    tmp = query+resp

    #print(tmp)
    #tmp_ = re.sub(u'[^\u4e00-\u9fa5]','',tmp)
    #print(tmp_)
    #if tmp_ in existed:
    #  print('stop in duplicate remov')
    #  pass
    #length
    if lqu>15 or lre>20 or lqu<2 or lre<2:
      #print('stop in length control')
      pass
    #website
    elif re.findall(u'\.com|\.cn|\.top|\.org|http|html|www|.exe"]',tmp):
      #print(re.findall(u'.com|.cn|.top|.|.org',tmp))
      #print('stop in website filter')
      pass
    elif re.findall(u'[^\u4e00-\u9fa5,.:;\'"?!，。、？：；“”‘’！《》a-zA-Z\s\d]',tmp):
      pass
    elif query_cutted==resp_cutted:
      pass
    #number
    #elif re.findall(u'\d',tmp):
      #print(re.findall(u'\d',tmp))
      #print('stop in number filter')
     # pass
    else:
      #existed.add(tmp_)
      #print(existed)
      result_f.write('Q:'+query_cutted+'\n'+'A:'+resp_cutted+'\n')
      i1 += 1
    query,resp = f.readline(),f.readline()
    #if i0>50:
    #  break
  #print(existed)
  f.close()
  result_f.close()
  print(i0,i1)
def minganci(path):
  f = open('minganci.txt')
  mg_words = f.readlines()
  f.close()
  mg_words = [ele.strip() for ele in mg_words]
  f = open(path)
  result_f = open(path+'.clear_dirty','w')
  q,a = f.readline(), f.readline()
  n0,n1 = 0,0
  while q and a:
    n0 += 1
    written = True
    for w in mg_words:
      if q.find(w)>-1 or a.find(w)>-1:
         written = False
         break
    if written:
      n1 += 1
      result_f.write(q+a)
    q,a = f.readline(),f.readline()
  f.close()
  result_f.close()
  print(n0,n1)
    
if  __name__ == "__main__":
  json2txt('/home/zyma/work/ruisheng.final')
  minganci('/home/zyma/work/ruisheng.final.processed')
  weibo('/home/zyma/work/ruisheng.final.processed.clear_dirty')
  #duplicate_remv('/home/zyma/work/weibos.txt.processed.processed')

  
    
        
