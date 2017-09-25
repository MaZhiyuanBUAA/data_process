#-*-coding:utf-8-*-
import sys,re
import math,json
import collections
from collections import defaultdict
reload(sys)
sys.setdefaultencoding('utf-8')
def main():
  if len(sys.argv)<2:
    print('No file !')
    return
  program = sys.argv[0]
  source_f = sys.argv[1]
  vocab_f = sys.argv[2]

  f = open(vocab_f)
  vocab_ = f.readlines()
  f.close()

  try:
    target_f = sys.argv[3]
  except:
    target_f = 'static_results.txt'
  vocab = {}
  #read data
  f = open(source_f,'r')
  sources = f.readlines()
  f.close()
  for ele in sources:
    words = ele.split()
    for w in words:
      try:
        vocab[w] += 1
      except:
        vocab[w] = 1
  vocab_l = sorted(vocab.items(),key=lambda x:x[1],reverse=True)
  print(vocab_l[:100])
  with open(target_f,'w') as f:
    for ele in vocab_l:
      #f.write(vocab_[int(ele[0])]+':'+str(math.log(ele[1],10))+'\n')
      f.write(ele[0]+':'+str(math.log(ele[1],10))+'\n')
def short_sentences(source_f):
  f = open(source_f)
  sentences = f.readlines()
  f.close()
  l = len(sentences)
  frequency = defaultdict(int)
  for ind,ele in enumerate(sentences):
    short_sents = re.split(u'[，。：？；‘’“”【】/\,\\?|]',ele.decode('utf-8'))
    if (ind+1)%10000==0:
      print('processing line %d\%d'%(ind,l))
    for ele in short_sents:
      frequency[ele] += 1
  items = frequency.items()
  items = sorted(items,key=lambda x:-x[1])
  for ind, ele in enumerate(items):
    if ele[1]==5:
      break
  items = items[:ind]
  frequency = collections.OrderedDict(items)
  f = open('result_of_%s'%(source_f),'w')
  s = json.dumps(frequency,indent=2,ensure_ascii=False)
  f.write(s)
  f.close()
if __name__ == '__main__':
  source_f = sys.argv[1]
  short_sentences(source_f)
  #main()
