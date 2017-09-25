#coding:utf-8
import matplotlib.pyplot as plt
import sys

f1 = sys.argv[1]
f2 = sys.argv[2]

f = open(f1)
d0 = f.readlines()
f.close()

f = open(f2)
d1 = f.readlines()
f.close()

l0 = []
l1 = []
for ele in d0:
  item = ele.split(':')
  if len(item)==2:
    l0.append(item)
for ele in d1:
  item = ele.split(':')
  if len(item)==2:
    l1.append(item)

dict_d0 = dict(l0)
dict_d1 = dict(l1)

axis0 = []
axis1 = []
for ele in dict_d1.keys():
  axis0.append(float(dict_d0[ele]))
  axis1.append(float(dict_d1[ele]))
plt.plot(axis0,axis1)
plt.savefig('result.png')
