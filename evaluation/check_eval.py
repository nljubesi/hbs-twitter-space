#!/usr/bin/python
#-*-coding:utf8-*-


from collections import defaultdict

c=0
vars=[]
values=[]
tp_dict=defaultdict(int)
tn_dict=defaultdict(int)
fp_dict=defaultdict(int)
fn_dict=defaultdict(int)


for line in open("evalrandom500_checked.tsv", "r"):
    line = line.rstrip("\r\n")
    line = line.split("\t")
    myvarline=line[1:]
    c+=1
    if c==1:
        vars=myvarline

for line in open("evalrandom500_checked.tsv", "r"):
    line = line.rstrip("\r\n")
    line = line.split("\t")
    myvarline=line[1:]
    c+=1
    if not c==1:
        for index, myvar in enumerate(vars):
            myvalue=myvarline[index]

            if not myvalue =="-" and not myvalue.endswith("(FP)"):
                tp_dict[myvar]+=1
            elif myvalue.endswith("(FP)"):
                fp_dict[myvar]+=1
            elif myvalue.endswith("-"):
                tn_dict[myvar]+=1
            else:
                fn_dict[myvar]+=1

print "\t", "TP","\t", "FP","\t", "TN","\t", "FN"
for myvar in vars:
    print myvar, "\t", tp_dict[myvar], fp_dict[myvar], tn_dict[myvar], fn_dict[myvar]



