#!/usr/bin/python
#-*-coding:utf8-*-


import gzip

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

## Open files for writing
lexicon_dirs='../../lexicons/apertium'
vmfverbs=gzip.open('../custom-lexicons/verbs-vmf-stem-lexicon.gz','w')

# Open dicts for preventing duplicates
vmfdict={}

# Iterate over Apertium lexicoans
for myfile in [lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz', lexicon_dirs+'/apertium-hbs.hbs_SR_purist.mte.gz']:
    for line in gzip.open(myfile):
      token,lemma,tag=line.decode('utf8').split('\t')[:3]
      if tag.startswith(u"Vmf"):
          tokennodia = remove_diacritics(token)
          tokennodia = tokennodia.rstrip("cu").rstrip("ces").rstrip("ce").rstrip("cemo").rstrip("cete").rstrip("ce")
          vmfdict[tokennodia]=1


def writeinfile(mydict,myout):
    for token in mydict:
        myout.write(token.encode("utf8")+"\n")
    return myout
    myout.close()

writeinfile(vmfdict,vmfverbs)

## problem for evaluation:
## not every -og/eg can become -oga:
#  "Iz [nekog] švajcarsk[og] sela bi bilo korektnije vs lako je naci nek[og] sa kim cete ziveti tesko je pronaci [nekog] u kome cete ziveti"
