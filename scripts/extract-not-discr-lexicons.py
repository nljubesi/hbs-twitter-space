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
# desavati=gzip.open('../custom-lexicons/desiti-desavati.gz','w')
# dogadjati=gzip.open('../custom-lexicons/dogoditi-dogadjati.gz','w')

# Open dicts for preventing duplicates
presverbsdict, chdict, infverbsdict, genitiv_og_dict, verbs_dict, vmfverbsdict, modalsdict ={},{},{},{},{},{},{}
# desavati_dict, dogadjati_dict = {},{}

modallemmas=[u"moći",u"znati",u"trebati",u"hteti",u"htjeti",u"morati",u"smeti",u"smjeti",u"želeti",u"željeti",u"voleti",u"voljeti"]


def get_into_dict(myitem, mydict):
    nodiaitem = remove_diacritics(myitem)
    mydict[myitem.lower()]=1
    mydict[nodiaitem.lower()]=1
    return mydict

def writeinfile(mydict,myout):
    for token in sorted(mydict):
        myout.write(token.encode("utf8")+"\n")
    myout.close()
    return myout

# Iterate over Apertium lexicoans
for myfile in [lexicon_dirs+'/hrLex_v1.0.gz', lexicon_dirs+'/srLex_v1.0.gz']:
    for line in gzip.open(myfile):
      token,lemma,tag=line.decode('utf8').split('\t')[:3]
      ## if "ć" or "č" are present in the token:
      if u"ć" in token or u"č" in token:
          chdict[token.lower()]=1
      ## if token is a verb:
      ## if ends with -og or -eg, if it's Adj or Number  and if its masculin of neutrum singular, save it to the dict
      if (token.endswith(u"og") or token.endswith(u"eg")) and \
              (tag.startswith(u"A") or tag.startswith(u"M")) and \
              (u"msg" in tag or u"nsg" in tag):
          # for now ignore pronouns vtag.startswith("P") because mostly no -a drop (idea: another function only for pronouns)
          get_into_dict(token,genitiv_og_dict)


      # if lemma ==u"događati" or lemma==u"dogoditi":
      #     get_into_dict(lemma,dogadjati_dict)
      # if lemma ==u"desiti" or lemma==u"dešavati":
      #     get_into_dict(lemma,desavati_dict)

      if tag.startswith(u"V"):
          get_into_dict(token,verbs_dict)
          if lemma in modallemmas:
            get_into_dict(token,modalsdict)

         ## if token is an infinitiv:
          if tag.startswith(u'Vmn'):
              get_into_dict(token,verbs_dict)
          ## if token is in present tense:
          elif tag.startswith(u"Vmr"):
              get_into_dict(token,presverbsdict)
          #if token is infinitiv such syntetic future
          elif tag.startswith(u"Vmf"):
              get_into_dict(token,vmfverbsdict)


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
