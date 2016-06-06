#!/usr/bin/python
#-*-coding:utf8-*-

from __future__ import division
import glob


output = open("precision.txt", "w")
for file in glob.glob("eval_tp_fp/*tsv"):
    tp=0
    fp=0
    myfile = open(file, "r")
    for line in myfile:
        line =line.split("\t")
        if len(line)==4:
            if line[2]=="1":
                tp+=1
            elif line[2]=="":
                if not line[3]=="":
                    fp+=1

    precision = str(round(tp/(tp+fp),2))
    output.write(str(file)+"\t"+str(tp)+"\t"+str(fp)+"\t"+precision+"\n")


