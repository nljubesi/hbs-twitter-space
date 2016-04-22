#!/usr/bin/python
#-*-coding:utf8-*-


import gzip

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

lexicon_dirs='../lexicons/apertium'
presverbs=gzip.open('presverbs/presverbs.gz','w')
ch=gzip.open('ch/ch.gz','w')
infverbs=gzip.open('inf/inf.gz','w')
syntinfverbs = gzip.open('syntinf/syntinf.gz','w')
genitiv_og=gzip.open('genitiv_og/genitiv_og.gz','w')
verbs=gzip.open('verbs/verbs.gz', 'w')

presverbsdict, chdict, infverbsdict, syntinfverbsdict, genitiv_og_dict, verbs_dict = {},{},{},{},{},{}

for myfile in ['../lexicons/apertium/apertium-hbs.hbs_HR_purist.mte.gz', '../lexicons/apertium/apertium-hbs.hbs_SR_purist.mte.gz']:
    for line in gzip.open(myfile):
      token,lemma,tag=line.decode('utf8').split('\t')[:3]
      if u"ć" or u"č" in token:
          chdict[token]=1
      # if verb:
      if tag.startswith(u"V"):
          tokennodia=remove_diacritics(token)
          verbs_dict[tokennodia]=1
      # if infinitiv:
      if tag == u'Vmn':
          tokennodia=remove_diacritics(token)
          infverbsdict[tokennodia]=1
      ## if present:
      elif tag.startswith(u"Vmr"):
          tokennodia = remove_diacritics(token)
          presverbsdict[tokennodia]=1
      ## if genitiv ending with -og
      elif token.endswith(u"og") and u"msgy" in tag or u"nsgy" in tag:
          # ako samo pridjevi: add y poslije (m|n)sg (slijepoga	slijep	Agpmsgy)
          # problem "Iz nekog švajcarskog sela bi bilo korektnije vs lako je naci nekog sa kim cete ziveti tesko je pronaci nekog u kome cete ziveti"
          tokennodia = remove_diacritics(token)
          genitiv_og_dict[tokennodia]=1


def writeinfile(mydict,myout):
    for token in mydict:
        myout.write(token.encode("utf8")+"\n")

writeinfile(chdict,ch)
writeinfile(verbs_dict,verbs)
writeinfile(infverbsdict,infverbs)
writeinfile(presverbsdict,presverbs)
writeinfile(genitiv_og_dict,genitiv_og)

ch.close()
verbs.close()
infverbs.close()
presverbs.close()
genitiv_og.close()

