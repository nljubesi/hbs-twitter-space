#!/usr/bin/python
#-*-coding:utf8-*-

import gzip
import re
token_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+|\w+',re.UNICODE)
yat_lexicon=dict([e[:-1].split('\t') for e in gzip.open('yat-lexicon/apertium-yat.gz')])

def tokenize(text):
  return token_re.findall(text)

def yat(text):
  distr={}
  for token in tokenize(text.lower()):
    if token in yat_lexicon:
      distr[yat_lexicon[token]]=distr.get(yat_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]

out=gzip.open('hrsrTweets.var.gz','w')
for line in gzip.open('hrsrTweets.gz'):
  tid,user,time,lang,lon,lat,text=line[:-1].decode('utf8').split('\t')
  out.write(line[:-1]+'\t'+yat(text)+'\n')
out.close()
