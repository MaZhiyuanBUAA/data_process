#coding:utf-8
import jieba
import json
import random
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

def json2txt(data_path,save_dir,data_size=20000000,test_size=1000):
    ftrain = open(os.path.join(save_dir,'train.in'),'w')
    ftest = open(os.path.join(save_dir,'test.in'),'w')
    f = open(data_path,'rb')
    sentence = f.readline()
    testID = set(random.sample(range(data_size),test_size))
    counter = 1
    while sentence:
        itmesFormatJs = json.loads(sentence.decode('utf-8'))
        post = itmesFormatJs['post'].replace('\n', '')
        comment = itmesFormatJs['cmnt'][0]['content'].replace('\n', '')
        #print(list(post))
        post = ' '.join(list(post))
        #print(post)
        #break
        comment = ' '.join(list(comment))

        if counter in testID:
            try:
                ftest.write(post+'\n'+comment+'\n')
                counter += 1
            except:
                pass
        else:
            try:
                ftrain.write(post+'\n'+comment+'\n')
                counter += 1
            except:
                pass
        if counter%100000 == 0:
            print('processing line %d'%counter)
        sentence = f.readline()
    f.close()
    ftest.close()
    ftrain.close()
def json2text_google(data_path,save_dir,k=5,data_size=2000000,test_size=10000):
    ftrain = open(os.path.join(save_dir,'train.in'),'w')
    ftest = open(os.path.join(save_dir,'test.in'),'w')
    f = open(data_path,'rb')
    sentence = f.readline()
    testID = set(random.sample(range(data_size),test_size))
    counter = 1
    while counter<=data_size:
        itmesFormatJs = json.loads(sentence.decode('utf-8'))
        post = itmesFormatJs['post'].replace('\n', '')
        comment = itmesFormatJs['cmnt'][0]['content'].replace('\n', '')
        #print(list(post))
        #post = ' '.join(list(post))#if add space
        #print(post)
        #break
        #comment = ' '.join(list(comment))#if add space

        if counter in testID:
            try:
                ftest.write(post+'\n'+comment+'\n')
                counter += 1
            except:
                pass
        else:
            try:
                ftrain.write(post+'\n'+comment+'\n')
                counter += 1
            except:
                pass
        if counter%100000 == 0:
            print('processing line %d'%counter)
        sentence = f.readline()
    f.close()
    ftest.close()
    ftrain.close()
def text2dataSet(sents,save2='source_'):
    f0 = open(save2+'train.in','w')
    f1 = open(save2+'test.in','w')
    f2 = open(save2+'test_source.txt','w')
    f3 = open(save2+'test_target.txt','w')
    pair_size = len(sents)//2
    inds = range(pair_size)
    random.shuffle(inds)
    train_inds = inds[:-2000]
    test_inds = inds[-2000:-1000]
    tinds = inds[-1000:]
    for ele in train_inds:
        f0.write(sents[2*ele]+'\n'+sents[2*ele+1]+'\n')

    for ele in test_inds:
        f1.write(sents[2*ele]+'\n'+sents[2*ele+1]+'\n')
   
    for ele in tinds:
        f2.write(sents[2*ele]+'\n')
        f3.write(sents[2*ele+1]+'\n')
    f0.close()
    f1.close()
    f2.close()
    f3.close()
#unit test
if __name__ == '__main__':
    # train_set,test_set = prepaire_digit_data('minitest.txt','vocab.txt',100)
    # train_set,test_set = buid_set(train_set),buid_set(test_set)
    # print(test_set)
    json2txt('/home/zyma/work/ruisheng.final','/home/zyma/work',10000000,1000)

