#!/usr/bin/python
#-*-coding:utf8-*-
import gzip
import sys
from collections import defaultdict

lexicon_dirs='../../lexicons/apertium'

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(token):
  result=''
  for char in token:
    result+=dia.get(char,char)
  return result

log=open('log','w')
hr=defaultdict(int)
#sr={}
for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  #if token not in hr:
  tag = tag.rstrip("\n")
  if tag == u"Ncmsn" and token.endswith(u"ist"):
    sys.stdout.write(token.encode('utf8')+'\n')
    dia_token=remove_diacritics(token)
    if dia_token!=token:
        sys.stdout.write(dia_token.encode('utf8')+'\n')
