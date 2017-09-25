#coding:utf-8

import json
import re
import random
from collections import  defaultdict
from itertools import chain

def label_analysis():
  f = open('minitest.txt')
  l = set()
  d = f.readline()
  i = 0
  while d:
    i += 1
    dd = json.loads(d)
    try:
      ad = re.findall('/.+?/',dd['url'])[0]
      l.add(ad)
    except:
      pass
     #print(dd['url'])
    d = f.readline()
    #if i>1000000:
    #  break
  print(l)

def get_samples():
  f = open('ruisheng.final')
  labels = defaultdict(list)
  d = f.readline()
  i = 0
  while d:
    i += 1
    dd = json.loads(d)
    try:
      label = re.findall('/.+?',dd['url'])[0]
    except:
      label = 'other'
    labels[label].append(i)
    d = f.readline()
  f.close()
  sample_f = open('minitest.txt','w')
  for k in labels.keys():
    print('%s,%d'%(k,len(labels[k])))
    labels[k] = random.sample(labels[k],2000)
    
  f = open('ruisheng.final')
  indexs = list(chain(*labels.values()))
  indexs.sort(reverse=True)
  i = 0
  d = f.readline()
  index = indexs.pop()
  while d:
    i += 1
    if i==index:
      sample_f.write(d)
      try:
        index = indexs.pop()
      except:
        break
    else:
      d = f.readline()
  sample_f.close()
  f.close()
    
  
if __name__ == '__main__':
  get_samples()
  #label_analysis() 
