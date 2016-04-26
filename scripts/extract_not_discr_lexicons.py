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

ch=gzip.open('../custom-lexicons/ch-lexicon.gz','w')
verbs=gzip.open('../custom-lexicons/verbs-lexicon.gz', 'w')
infverbs=gzip.open('../custom-lexicons/verbs-inf-lexicon.gz','w')
presverbs=gzip.open('../custom-lexicons/verbs-pres-lexicon.gz','w')
genitiv_og=gzip.open('../custom-lexicons/genitiv-og-eg-lexicon.gz','w')

# Open dicts for preventing duplicates
presverbsdict, chdict, infverbsdict, genitiv_og_dict, verbs_dict = {},{},{},{},{}

# Iterate over Apertium lexicoans
for myfile in [lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz', lexicon_dirs+'/apertium-hbs.hbs_SR_purist.mte.gz']:
    for line in gzip.open(myfile):
      token,lemma,tag=line.decode('utf8').split('\t')[:3]
      ## if "ć" or "č" are present in the token:
      if u"ć" in token or u"č" in token:
          chdict[token]=1
      ## if token is a verb:
      if tag.startswith(u"V"):
          tokennodia=remove_diacritics(token)
          verbs_dict[tokennodia]=1
      ## if token is an infinitiv:
      if tag == u'Vmn':
          tokennodia=remove_diacritics(token)
          infverbsdict[tokennodia]=1
      ## if token is in present tense:
      elif tag.startswith(u"Vmr"):
          tokennodia = remove_diacritics(token)
          presverbsdict[tokennodia]=1
      ## if ends with -og or -eg, if it's Adj, Number or Pronoun and if its masculin of neutrum singular, save it to the dict
      elif (token.endswith(u"og") or token.endswith(u"eg")) and \
              (tag.startswith("A") or tag.startswith("M") or tag.startswith("P")) and \
              (u"msg" in tag or u"nsg" in tag):
          tokennodia = remove_diacritics(token)
          genitiv_og_dict[tokennodia]=1


def writeinfile(mydict,myout):
    for token in mydict:
        myout.write(token.encode("utf8")+"\n")
    myout.close()
    return myout


writeinfile(chdict,ch)
writeinfile(verbs_dict,verbs)
writeinfile(infverbsdict,infverbs)
writeinfile(presverbsdict,presverbs)
writeinfile(genitiv_og_dict,genitiv_og)

## problem for evaluation:
## not every -og/eg can become -oga:
#  "Iz [nekog] švajcarsk[og] sela bi bilo korektnije vs lako je naci nek[og] sa kim cete ziveti tesko je pronaci [nekog] u kome cete ziveti"
