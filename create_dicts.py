#!/usr/bin/python
#-*-coding:utf8-*-


import gzip
import re
from collections import defaultdict

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

lexicon_dirs='../lexicons/apertium'
#ch_dict,infverbs,syntinfverbs,modalsdict,genitiv_og = defaultdict(int),defaultdict(int),defaultdict(int),defaultdict(int),defaultdict(int)
#genitivoga_re=re.compile(r'og\t\w+\t\w+(m|n)sg(y)?$',re.UNICODE)
presverbs=gzip.open('presverbs/presverbs.gz','w')
ch=gzip.open('ch/ch.gz','w')
infverbs =gzip.open('inf/inf.gz','w')
syntinfverbs = gzip.open('syntinf/syntinf.gz','w')
genitiv_og=gzip.open('genitiv_og/genitiv_og.gz','w')
verbs=gzip.open('verbs/verbs.gz', 'w')
    #= defaultdict(int),defaultdict(int),defaultdict(int),defaultdict(int),defaultdict(int)


for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if u"ć" or u"č" in token:
      ch.write(token.encode("utf8")+"\n")
      #ch_dict[token]+=1
  ## if infinitiv with -i
  if tag.startswith(u"V"):
      tokennodia = remove_diacritics(token)
      verbs.write(tokennodia.encode("utf8")+"\n")
  if tag == u'Vmn':
      tokennodia = remove_diacritics(token)
      #infverbs[tokennodia]+=1
      infverbs.write(tokennodia.encode("utf8")+"\n")
  ## if presäns:
  elif tag.startswith(u"Vmr"):
      tokennodia = remove_diacritics(token)
      infile=tokennodia.encode("utf8")+"\t"+tag.encode("utf8")+"\n".replace("\n\n", "\n")
      presverbs.write(infile)
      #presverbs[tokennodia]+=tag
  ## if genitiv ending with og
  elif token.endswith(u"og") and u"msgy" in tag or u"nsgy" in tag:
      # ako samo pridjevi: add y poslije (m|n)sg (slijepoga	slijep	Agpmsgy)
      # problem "Iz nekog švajcarskog sela bi bilo korektnije vs lako je naci nekog sa kim cete ziveti tesko je pronaci nekog u kome cete ziveti"
      tokennodia = remove_diacritics(token)
      genitiv_og.write(tokennodia.encode("utf8")+"\n")

for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_SR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if u"ć" or u"č" in token:
      ch.write(token.encode("utf8")+"\n")
      #ch_dict[token]+=1
  ## if infinitiv with -i
  if tag.startswith(u"V"):
      tokennodia = remove_diacritics(token)
      verbs.write(tokennodia.encode("utf8")+"\n")
  if tag == u'Vmn':
      tokennodia = remove_diacritics(token)
      #infverbs[tokennodia]+=1
      infverbs.write(tokennodia.encode("utf8")+"\n")
  ## if presäns:
  elif tag.startswith(u"Vmr"):
      tokennodia = remove_diacritics(token)
      #if len(tag) >1 and len(tokennodia)>1:
      infile=tokennodia.encode("utf8")+"\t"+tag.encode("utf8")+"\n".replace("\n\n", "\n")
      presverbs.write(infile)
      #presverbs[tokennodia]+=tag
  ## if genitiv ending with og
  elif token.endswith(u"og") and u"msgy" in tag or u"nsgy" in tag:
      # ako samo pridjevi: add y poslije (m|n)sg (slijepoga	slijep	Agpmsgy)
      # problem "Iz nekog švajcarskog sela bi bilo korektnije vs lako je naci nekog sa kim cete ziveti tesko je pronaci nekog u kome cete ziveti"
      tokennodia = remove_diacritics(token)
      genitiv_og.write(tokennodia.encode("utf8")+"\n")
  elif tag.startswith(u'Vmf'):
      tokennodia = remove_diacritics(token)
      syntinfverbs.write(tokennodia.encode("utf8")+"\n")
