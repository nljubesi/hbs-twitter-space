#!/usr/bin/python
#-*-coding:utf8-*-

## Script for extracting customized dictionaries for the variables which are not necessarily different in SR and HR

import gzip

## Open files for writing
lexicon_dirs='../../lexicons/apertium'
modals=gzip.open('../custom-lexicons/modalverbs-lexicon.gz','w')
ch=gzip.open('../custom-lexicons/ch-lexicon.gz','w')
verbs=gzip.open('../custom-lexicons/verbs-lexicon.gz', 'w')
infverbs=gzip.open('../custom-lexicons/verbs-inf-lexicon.gz','w')
presverbs=gzip.open('../custom-lexicons/verbs-pres-lexicon.gz','w')
genitiv_og=gzip.open('../custom-lexicons/genitiv-og-eg-lexicon.gz','w')
vmfverbs=gzip.open('../custom-lexicons/verbs-vmf-lexicon.gz','w')
desavati=gzip.open('../custom-lexicons/desiti-desavati.gz','w')
dogadjati=gzip.open('../custom-lexicons/dogoditi-dogadjati.gz','w')

# Open dicts for preventing duplicates
presverbsdict, chdict, infverbsdict, genitiv_og_dict, verbs_dict, vmfverbsdict, modalsdict ={},{},{},{},{},{},{}
desavati_dict, dogadjati_dict = {},{}

modallemmas=[u"moći",u"znati",u"trebati",u"hteti",u"htjeti",u"morati",u"smeti",u"smjeti",u"želeti",u"željeti",u"voleti",u"voljeti"]

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}

## Function for replacing diacritics with their diacrtitic-free equivalents
def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

## Function for storing lowercased words into the dict
def get_into_dict(myitem, mydict):
    nodiaitem = remove_diacritics(myitem)
    mydict[myitem.lower()]=1
    mydict[nodiaitem.lower()]=1
    return mydict

## Function for writing the files (customized dictionaries)
def writeinfile(mydict,myout):
    for token in sorted(mydict):
        myout.write(token.encode("utf8")+"\n")
    myout.close()
    return myout

# Iterate over the apertium lexicoans
for myfile in [lexicon_dirs+'/hrLex_v1.0.gz', lexicon_dirs+'/srLex_v1.0.gz']:
    for line in gzip.open(myfile):
      token,lemma,tag=line.decode('utf8').split('\t')[:3]
      ## If "ć" or "č" are present in the token, store the lowercased token into the dict
      if u"ć" in token or u"č" in token:
          chdict[token.lower()]=1
      ## If ends with -og or -eg, if it's Adj or Number  and if its masculin of neutrum singular, save it to the dict
      if (token.endswith(u"og") or token.endswith(u"eg")) and \
              (tag.startswith(u"A") or tag.startswith(u"M")) and \
              (u"msg" in tag or u"nsg" in tag):
          get_into_dict(token,genitiv_og_dict)
      ## If lemma is događati,dogoditi -> store all its token in the dict
      if lemma ==u"događati" or lemma==u"dogoditi":
          get_into_dict(token,dogadjati_dict)
      ## If lemma is desiti,dešavati -> store all its token in the dict
      if lemma ==u"desiti" or lemma==u"dešavati":
          get_into_dict(token,desavati_dict)
      ## If the tag starts with "V", the token is a verb - store it in the verbs_dict

      if tag.startswith(u"V"):
          get_into_dict(token,verbs_dict)
          ## If the lemma is a modal verb, store all its token in modalsdict
          if lemma in modallemmas:
            get_into_dict(token,modalsdict)
         ## If the tag is an infinitiv, store the token having this tag in the infverbsdict
          if tag.startswith(u'Vmn'):
              get_into_dict(token,infverbsdict)
         ## If the tag means "present tense", store the token having this tag in the presverbsdict
          elif tag.startswith(u"Vmr"):
              get_into_dict(token,presverbsdict)
         ## If the tag means "synthetic future", store the token having this tag in the vmfverbsdict
          elif tag.startswith(u"Vmf"):
              get_into_dict(token,vmfverbsdict)


writeinfile(chdict,ch)
writeinfile(verbs_dict,verbs)
writeinfile(infverbsdict,infverbs)
writeinfile(presverbsdict,presverbs)
writeinfile(genitiv_og_dict,genitiv_og)
writeinfile(vmfverbsdict,vmfverbs)
writeinfile(modalsdict,modals)
writeinfile(dogadjati_dict,dogadjati)
writeinfile(desavati_dict,desavati)
