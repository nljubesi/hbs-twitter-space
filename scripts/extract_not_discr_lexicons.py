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
modals=gzip.open('../custom-lexicons/modalverbs-lexicon.gz','w')
ch=gzip.open('../custom-lexicons/ch-lexicon.gz','w')
verbs=gzip.open('../custom-lexicons/verbs-lexicon.gz', 'w')
infverbs=gzip.open('../custom-lexicons/verbs-inf-lexicon.gz','w')
presverbs=gzip.open('../custom-lexicons/verbs-pres-lexicon.gz','w')
genitiv_og=gzip.open('../custom-lexicons/genitiv-og-eg-lexicon.gz','w')
vmfverbs=gzip.open('../custom-lexicons/verbs-vmf-lexicon.gz','w')

# Open dicts for preventing duplicates
presverbsdict, chdict, infverbsdict, genitiv_og_dict, verbs_dict, vmfverbsdict, modalsdict = {},{},{},{},{},{},{}

# for creating the modals list with duplicates & diacritics:
#$ zgrep -E "\t(moći|znati|trebati|hteti|morati|smeti|želeti|voleti)\tV" apertium-hbs.hbs_SR_purist.mte.gz |cut -f 1 >  ../../hbs-twitter-space/srmodals.txt
#$ zgrep -E "\t(moći|znati|trebati|htjeti|morati|smjeti|željeti|voljeti)\tV" apertium-hbs.hbs_HR_purist.mte.gz |cut -f 1 >  ../../hbs-twitter-space/hrmodals.txt
#$ cat hrmodals.txt srmodals.txt |sort|uniq > modals.txt


modallemmas=[u"moći",u"znati",u"trebati",u"hteti",u"htjeti",u"morati",u"smeti",u"smjeti",u"želeti",u"željeti",u"voleti",u"voljeti"]


# Iterate over Apertium lexicoans
for myfile in [lexicon_dirs+'/hrLex_v1.0.gz', lexicon_dirs+'/srLex_v1.0.gz']:
    for line in gzip.open(myfile):
      token,lemma,tag=line.decode('utf8').split('\t')[:3]
      ## if "ć" or "č" are present in the token:
      if u"ć" in token or u"č" in token:
          chdict[token.lower()]=1
      ## if token is a verb:
      if tag.startswith(u"V"):
          tokennodia=remove_diacritics(token)
          verbs_dict[token.lower()]=1
          verbs_dict[tokennodia.lower()]=1
      ## if token is an infinitiv:
      if tag == u'Vmn':
          tokennodia=remove_diacritics(token)
          infverbsdict[token.lower()]=1
          infverbsdict[tokennodia.lower()]=1
      ## if token is in present tense:
      elif tag.startswith(u"Vmr"):
          tokennodia = remove_diacritics(token)
          presverbsdict[token.lower()]=1
          presverbsdict[tokennodia.lower()]=1

      elif tag.startswith(u"Vmf"):
          tokennodia = remove_diacritics(token)
          vmfverbsdict[token.lower()]=1
          vmfverbsdict[tokennodia.lower()]=1
      ## if ends with -og or -eg, if it's Adj or Number  and if its masculin of neutrum singular, save it to the dict
      elif (token.endswith(u"og") or token.endswith(u"eg")) and \
              (tag.startswith("A") or tag.startswith("M")) and \
              (u"msg" in tag or u"nsg" in tag):
          # for now ignore pronouns vtag.startswith("P") because mostly no -a drop (idea: another function only for pronouns)
          tokennodia = remove_diacritics(token)
          genitiv_og_dict[token.lower()]=1
          genitiv_og_dict[tokennodia.lower()]=1
      elif lemma in modallemmas:
          tokennodia = remove_diacritics(token)
          modalsdict[token.lower()]=1
          modalsdict[tokennodia.lower()]=1


def writeinfile(mydict,myout):
    for token in sorted(mydict):
        myout.write(token.encode("utf8")+"\n")
    myout.close()
    return myout


writeinfile(chdict,ch)
writeinfile(verbs_dict,verbs)
writeinfile(infverbsdict,infverbs)
writeinfile(presverbsdict,presverbs)
writeinfile(genitiv_og_dict,genitiv_og)
writeinfile(vmfverbsdict,vmfverbs)
writeinfile(modalsdict,modals)


## problem for evaluation:
## not every -og/eg can become -oga:
#  "Iz [nekog] švajcarsk[og] sela bi bilo korektnije vs lako je naci nek[og] sa kim cete ziveti tesko je pronaci [nekog] u kome cete ziveti"
