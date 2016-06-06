#!/usr/bin/python
#-*-coding:utf8-*-

from __future__ import division
from collections import defaultdict

vars=[]
values=[]
tp_dict=defaultdict(int)
tn_dict=defaultdict(int)
fp_dict=defaultdict(int)
fn_dict=defaultdict(int)

accuracy=open("accuracy.txt", "w")

l=[]
for line in open("evalrandom500-checked.tsv", "r"):
    line = line.rstrip("\r\n")
    line = line.split("\t")
    l.append(line)

columntoraw=zip(*l)


vars=[]
for column in columntoraw[1:-2]:
    vars.append(column[0])
    for value in column[1:-2]:
        #print value
        if not value.endswith("(FP)") and not "-" in value:
            tp_dict[column[0]]+=1
        elif "(FP)" in value:
             fp_dict[column[0]]+=1
        elif "(FN)" in value:
             fn_dict[column[0]]+=1
        else:
             tn_dict[column[0]]+=1


for myvar in vars:
    acc=str(round((tp_dict[myvar]+tn_dict[myvar]+1)/(tp_dict[myvar]+fp_dict[myvar]+tn_dict[myvar]+fn_dict[myvar]+1),2))
    writein= str(myvar)+"\t"+ str(tp_dict[myvar])+"\t"+str(fp_dict[myvar])+"\t"+str(tn_dict[myvar])+"\t"+str(fn_dict[myvar])+"\t"+acc+"\n"
    accuracy.write(writein)

accuracy.close()



