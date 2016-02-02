#!/usr/bin/python
#-*-coding:utf8-*-

import gzip
import re
from collections import defaultdict
lexicon_dirs='../lexicons/apertium'

import sys
token_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+|\w+',re.UNICODE)
yat_lexicon=dict([e[:-1].split('\t') for e in gzip.open('yat-lexicon/apertium-yat.gz')])
kh_lexicon=dict([k[:-1].split('\t') for k in gzip.open('kh-lexicon/apertium-kh.gz')])
hdrop_lexicon=dict([k[:-1].split('\t') for k in gzip.open('drop-lexicon/apertium-hdrop.gz')])
rdrop_lexicon=dict([k[:-1].split('\t') for k in gzip.open('drop-lexicon/apertium-rdrop.gz')])
alltokensdict = defaultdict(int)
for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  alltokensdict[token]+=1

#TODO: rdrop lexicon is to be extended (apertium is not a good resource for this)
#TODO: Ldrop lexicon is to be made (apertium is not a good resource for this)



dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd'}
def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

def tokenize(text):
  return token_re.findall(text)


#---Start Phonetical Features-------------------------------------------------------------------------------------------

def yat(text):
  distr={}
  for token in tokenize(text.lower()):
    if token in yat_lexicon:
      distr[yat_lexicon[token]]=distr.get(yat_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]

def kh(text):
  distr={}
  for token in tokenize(text.lower()):
    if token in kh_lexicon:
      distr[kh_lexicon[token]]=distr.get(kh_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]

def hdrop(text):
  distr={}
  for token in tokenize(text.lower()):
    if token in hdrop_lexicon:
      distr[hdrop_lexicon[token]]=distr.get(hdrop_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]

def rdrop(text):
  distr={}
  for token in tokenize(text.lower()):
    if token in rdrop_lexicon:
      distr[rdrop_lexicon[token]]=distr.get(rdrop_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]

def c_ch(text):
  distr_ch,distr_c={},{}
  for token in tokenize(text.lower()):
      if u"č" in token and token not in alltokensdict:
          mod_token = token.replace(u"č",u"ć")
          if mod_token in alltokensdict:
              distr_ch[mod_token]=1
      if u"ć" in token and token not in alltokensdict:
          mod_token = token.replace(u"ć",u"č")
          if mod_token in alltokensdict:
              distr_c[mod_token]=1
  if len(distr_ch)>=1:
    return "ch_dev"
  if len(distr_c)>=1:
    return "c_dev"
  else:
    return "NA"


#---End Phonetical Features---------------------------------------------------------------------------------------------

#---Start Lexical Features----------------------------------------------------------------------------------------------

# TODO– te / pa, pa relative frequency (difficult because of te personal pronoun)
# TODO – ”treba da” vs. ”treba* da”

def sa_s(text):
    """" sa / s rule deviation
    #http://savjetnik.ihjj.hr/savjet.php?id=17
    #Prijedlog sa upotrebljava se samo ispred riječi koje počinju glasovima s, š, z, ž
    #other source http://jezicna-pomoc.lss.hr/jsavjeti.php?view=2: more complicated"""""

    #text = text.encode("utf8")
    text = text.lower()
    #s_re=re.search(r'\ssa(?!)((c|s|z|č|ć|š|ž|đ|dž)|\w(s|z|š|ž))',text)
    s_re_dev=re.search(r'\ss\s((s|z|š|ž)|(?!aeiou)(s|z|š|ž))',text)
    sa_re_dev=re.search(r'\ssa\s(?!((s|z|š|ž)|(?!aeiou)(s|z|š|ž)|mnom))',text)
    if s_re_dev:
        return "s_rule_dev"
    elif sa_re_dev:
        return "sa_rule_dev"
    else:
        return "NA"

def tko_ko(text):
    """" tko / ko """""
    text_withoutdia = remove_diacritics(text).lower()
    tko_re=re.search(r'\b(ne|gdje|ni|i|sva|koje)?tko\b',text_withoutdia)
    ko_re=re.search(r'\b(ne|ni|i|sva|koje)?ko\b',text_withoutdia)
    if tko_re:
        return "tko"
    elif ko_re:
        return "ko"
    else:
        return "NA"


def sta_sto(text):
    """" što / šta """""
    text_withoutdia = remove_diacritics(text).lower()
    sto_re=re.search(r'\b(sto)\b',text_withoutdia)
    sta_re=re.search(r'\b(sta)\b',text_withoutdia)
    if sto_re:
        return 'što'
    elif sta_re:
        return 'šta'
    else:
        return 'NA'

def da_je_li(text):
    text_withoutdia = remove_diacritics(text).lower()
    dali_re=re.search(r'\b(da li|dal)\b',text_withoutdia)
    jeli_re=re.search(r'\b(je li|jel)\b',text_withoutdia)
    if dali_re:
        return 'da_li'
    elif jeli_re:
        return 'je_li'
    else:
        return 'NA'

def usprkos(text):
    text_withoutdia = remove_diacritics(text).lower()
    if u'usprkos' in text_withoutdia:
        return 'usprkos'
    elif u'uprkos' in text_withoutdia:
        return 'uprkos'
    elif u'unatoc' in text_withoutdia:
        return 'unatoč'
    ## add premda?
    else:
        return "NA"


#---End Lexical Features -----------------------------------------------------------------------------------------------


out=gzip.open('hrsrTweets.var.gz','w')
for line in gzip.open('hrsrTweets.gz'):
  tid,user,time,lang,lon,lat,text=line[:-1].decode('utf8').split('\t')
  #myline = line[:-1].decode('utf8')
  out.write(line[:-1]+'\t'+yat(text)+'\t'+kh(text)+"\t"+hdrop(text)+"\t"+rdrop(text)+"\t"+c_ch(text)+"\t"+sa_s(text)+"\t"+tko_ko(text)+"\t"+sta_sto(text)+"\t"+da_je_li(text)+"\t"+usprkos(text)+'\n')

  #out.write(da_je_li(text))
  #sys.stdout.write(tko_ko(text).encode('utf8')+'\t'+text.encode('utf8')+'\n')
  #sys.stdout.write(da_je_li(text).encode('utf8')+'\t'+text.encode('utf8')+'\n')
  #sys.stdout.write(usprkos(text).encode('utf8')+'\t'+text.encode('utf8')+'\n')
  #sys.stdout.write(sa_s(text).encode('utf8')+'\t'+text.encode('utf8')+'\n')
#  sys.stdout.write(kh(text).encode('utf8')+'\t'+text.encode('utf8')+'\n')
  #print kh(text)+" "+text


out.close()
