#!/usr/bin/python
#-*-coding:utf8-*-


from __future__ import division
import gzip
import re
import codecs
from collections import defaultdict


dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

token_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+|\w+',re.UNICODE)
yat_lexicon=dict([e[:-1].split('\t') for e in gzip.open('yat-lexicon/apertium-yat.gz')])
kh_lexicon=dict([k[:-1].split('\t') for k in gzip.open('kh-lexicon/apertium-kh.gz')])
hdrop_lexicon=dict([h[:-1].split('\t') for h in gzip.open('drop-lexicons/apertium-hdrop.gz')])
rdrop_lexicon=dict([r[:-1].split('\t') for r in gzip.open('drop-lexicons/apertium-rdrop.gz')])
presverbs=dict([pres[:-1].split('\t') for pres in gzip.open('presverbs/presverbs.gz')])
st_lexicon=dict([st[:-1].split('\t') for st in gzip.open('st_lexicon/apertium_st.gz')])
diftong_lexicon=dict([diftong[:-1].split('\t') for diftong in gzip.open('diftong_v/apertium_diftong_lexicon.gz')])
stems_dict={stem.rstrip("\n"):1 for stem in codecs.open('ir_ov_is/inter_stem_lex.txt', 'r', 'utf8')}
ch_dict={stem.rstrip("\n"):1 for stem in gzip.open('ch/ch.gz')}
inf_dict={inf.rstrip("\n"):1 for inf in gzip.open('inf/inf.gz')}
syntinf_dict={syntinf.rstrip("\n"):1 for syntinf in gzip.open('syntinf/syntinf.gz')}
verbs_dict={verb.rstrip("\n"):1 for verb in gzip.open('verbs/verbs.gz')}
genitiv_og_dict={genitiv_og.rstrip("\n"):1 for genitiv_og in gzip.open('genitiv_og/genitiv_og.gz')}
ist_dict={ist.rstrip("\n"):1 for ist in gzip.open('ist/ist.gz')}

hrmonths = [remove_diacritics(x.split("\t")[1].rstrip("\n")).lower() for x in codecs.open("months/hr_months.txt", "r", "utf8")]
intmonths = [remove_diacritics(x.split("\t")[1].rstrip("\n")).lower() for x in codecs.open("months/int_months.txt", "r", "utf8")]


def tokenize(text):
  return token_re.findall(text)


##---Start Cleanining Features------------------------------------------------------------------------------------------


def clean(text,lang):
    automatic_re = re.search("(Objavio/la sam novu fotografiju|Just posted a photo|Today stats:|I just ousted|I'm at|I (just)? ?(voted|added)|via (Tumblr|Facebook)|I liked a @YouTube)",text)
    if automatic_re or "tweep" in "automatically checked by" in text:
        return "automatic"
    elif lang.startswith("en:1"):
         return "English tweet"
    elif lang.startswith("en:") and "if you" in text or " visit " in text:
         return "English tweet"

    else:
        if len(tokenize(text))==2:
             emoji_punct_website_re = re.search("^[^A-Za-z]+ ?http.+$",text,re.UNICODE)
             user_website_re = re.search("^@.+ ?http.+$",text,re.UNICODE)
             user_puncta = re.search("^@.+ ?[^A-Za-z]+$",text,re.UNICODE)
             user_punctb = re.search("[^A-Za-z]+ ?@.+?$",text,re.UNICODE)
             if emoji_punct_website_re or user_website_re:
                 return "noise website"
             elif user_puncta or user_punctb:
                 return "noise user"
             else:
                 return "NA"
        elif len(tokenize(text)) == 1:
            only_punct_re = re.search("^[^A-Za-z]+$",text,re.UNICODE)
            if "".join(tokenize(text)).startswith("http"):
                return "website"
            elif only_punct_re:
                return "is not alpha"
            else:
                return "NA"
        else:
            return "NA"
            ## Eventually:
            #other_non_bkms_tweets_re = re.search("\w+? ?(Follow me on|check (this)? ?out|you should|untitled)",text)
            #if other_non_bkms_tweets_re:
             #   return "other"


##--- End Cleanining Features-------------------------------------------------------------------------------------------

#---Start Phonetical Features-------------------------------------------------------------------------------------------

def yat(text):
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in yat_lexicon:
      distr[yat_lexicon[token]]=distr.get(yat_lexicon[token],0)+1
  if len(distr)==0:
    return 'NA'
  elif len(distr)==2:
    sdistr=sorted(distr.items(),key=lambda x:-x[1])
    if sdistr[0][1]==sdistr[1][1]:
        return 'NA'
    else:
        return sdistr[0][0]
  else:
    return distr.keys()[0]

def kh(text):
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in kh_lexicon:
      distr[kh_lexicon[token]]=distr.get(kh_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]


def hdrop(text):
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in hdrop_lexicon:
      distr[hdrop_lexicon[token]]=distr.get(hdrop_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]

def rdrop(text):
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in rdrop_lexicon:
      distr[rdrop_lexicon[token]]=distr.get(rdrop_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]


def st(text):
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in st_lexicon:
      distr[st_lexicon[token]]=distr.get(st_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]

def diftong(text):
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in diftong_lexicon:
      distr[diftong_lexicon[token]]=distr.get(diftong_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]


def c_ch(text):
  distr_ch,distr_c={},{}
  for token in tokenize(text.lower()):
      if u"č" in token and token not in ch_dict:
          mod_token = token.replace(u"č",u"ć")
          if mod_token in ch_dict:
              distr_ch[mod_token]=1
      if u"ć" in token and token not in ch_dict:
          mod_token = token.replace(u"ć",u"č")
          if mod_token in ch_dict:
              distr_c[mod_token]=1
  if len(distr_ch) ==1 and len(distr_ch) ==1:
      return "both č dev & ć dev"
  if len(distr_ch)==1:
    return "č dev"
  elif len(distr_c)==1:
    return "ć dev"
  else:
    return "NA"


# def ao_o(text):
#     #
#     # Many false positivs:
#
#     # proble,: vi
#     #pusto -> pustao, do->dao
#   distr_o, distr_ao=defaultdict(int), defaultdict(int)
#   for token in tokenize(text.lower()):
#     if token.endswith("ao"):
#         mod_token = remove_diacritics(token)
#         if token in verbs_dict:
#             distr_ao[token]+=1
#     elif token.endswith("o"):
#         mod_token = token[:-1]+"ao"
#         dia_mod_token = remove_diacritics(mod_token)
#         if dia_mod_token in verbs_dict:
#             distr_o[dia_mod_token]+=1
#   if len(distr_o) > 0 and len(distr_ao)>0:
#       return "ao and o end"
#   elif len(distr_o)>0:
#       return "o end"
#   elif len(distr_ao)>0:
#       return "ao end"
#   else:
#       return "NA"



#---End Phonetical Features---------------------------------------------------------------------------------------------

#---Start Lexical Features----------------------------------------------------------------------------------------------


def sa_s(text):

    """" sa / s rule deviation
    #http://savjetnik.ihjj.hr/savjet.php?id=17
    #Prijedlog sa upotrebljava se samo ispred riječi koje počinju glasovima s, š, z, ž
    #other (more complicated) source http://jezicna-pomoc.lss.hr/jsavjeti.php?view=2"""""

    text = text.lower()
    s_re_dev=re.search(r'\ss\s((s|z|š|ž)|(?!aeiou)(s|z|š|ž))',text)
    sa_re_dev=re.search(r'\ssa\s(?!((s|z|š|ž)|(?!aeiou)(s|z|š|ž)|mnom))',text)
    if s_re_dev and sa_re_dev:
        return "both sa & s rule dev"
    if s_re_dev:
        return "s rule dev"
    elif sa_re_dev:
        return "sa rule dev"
    else:
        return "NA"

def tko_ko(text):
    """" tko / ko """""
    text_withoutdia = remove_diacritics(text).lower()
    tko_re=re.search(r'\b(ne|gdje|ni|i|sva|koje)?tko\b',text_withoutdia)
    ko_re=re.search(r'\b(ne|ni|i|sva|koje)?ko\b',text_withoutdia)

    if tko_re and ko_re:
        return "both tko & ko"
    elif tko_re:
        return "tko"
    elif ko_re:
        return "ko"
    else:
        return "NA"


def sta_sto(text):
    """" što / šta """""
    #Note: što interrogative meaning same for all languages:  Sto da ne
    text_withoutdia = remove_diacritics(text).lower()
    sto_re=re.search(r'\b(sto)\b',text_withoutdia)
    sta_re=re.search(r'\b(sta)\b',text_withoutdia)
    if sto_re and sta_re:
        return "both što & šta"
    elif sto_re:
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
        return 'da li'
    elif jeli_re:
        return 'je li'
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
    else:
        return "NA"


def treba_da(text):

    """" treba da vs. treba* da """""
    text_withoutdia = remove_diacritics(text).lower()
    trebada=re.search(r'\b(treba|trebalo je|trebalo bi)\sda\b',text_withoutdia, re.UNICODE)
    trebaXsg=re.search(r'\btreba(m|s|mo|te|ju)\sda\b',text_withoutdia, re.UNICODE)
    trebaXpl=re.search(r'\btreba(la|o|li|le)\s(sam|si|je|smo|ste|su|bi)\sda\b',text_withoutdia, re.UNICODE)

    if trebada and (trebaXsg or trebaXpl):
        return "both treba da & trebaX da"
    elif trebada:
        return "treba da"
    elif trebaXsg or trebaXpl:
        return "trebaX da"
    else:
        return "NA"

def ist(text):
    distr_ist,distr_ista={},{}
    for token in tokenize(remove_diacritics(text).lower()):
        if token.endswith("ista"):
            if token[:-1] in ist_dict:
                distr_ista[token]=1
        elif token.endswith("ist"):
            if token in ist_dict:
                distr_ist[token]=1
    if len(distr_ist)==1:
        return "ist"
    elif len(distr_ista)==1:
        return "ista"
    else:
        return "NA"

def bre(text):
    """" bre /bolan / bona/ ba  """""
    text_withoutdia = remove_diacritics(text).lower()
    bre_re=re.search(r'\bbre\b',text_withoutdia)
    bolan_re=re.search(r'\b(bolan|bona)\b',text_withoutdia)
    ba_re=re.search(r'\bba\b',text_withoutdia)

    if bre_re:
        return 'bre'
    elif bolan_re:
        return 'bolan'
    elif ba_re:
        return 'ba'
    else:
        return 'NA'

def mnogo(text):
    text_withoutdia = remove_diacritics(text).lower()
    if u'mnogo' in text_withoutdia:
        return 'mnogo'
    elif u'puno' in text_withoutdia:
        return 'puno'
    elif u'vrlo' in text_withoutdia:
        return 'vrlo'
    elif u'jako' in text_withoutdia:
        return 'jako'
    else:
        return "NA"


def months(text):
    text_withoutdia = remove_diacritics(text).lower()
    hr, international = 0, 0
    for token in tokenize(text_withoutdia.lower()):
        if token in hrmonths:
            hr+=1
        elif token in intmonths:
            international+=1
    if hr > 0:
        return "HR months"
    elif international >0:
        return "international months"
    else:
        return "NA"

def tjedan(text):
    """" treba da vs. treba* da """""
    text_withoutdia = remove_diacritics(text).lower()
    tjedan_re=re.search(r'\b(tjed(an|na|no|nu|nom|ni|ana|nima))\b',text_withoutdia, re.UNICODE)
    sedmica_re=re.search(r'\bsedmic(a|u|i|om|e|ama)\b',text_withoutdia, re.UNICODE)
    nedjelja_re=re.search(r'\bnedjelj(a|u|i|om|e|ama)\b',text_withoutdia, re.UNICODE)
    nedelja_re=re.search(r'\bnedelj(a|u|i|om|e|ama)\b',text_withoutdia, re.UNICODE)

    if tjedan_re:
        return "tjedan"
    elif sedmica_re:
        return "sedmica"
    elif nedjelja_re:
        return "nedjelja"
    elif nedelja_re:
        return "nedelja"
    else:
        return "NA"


def drug(text):
    text_withoutdia = remove_diacritics(text).lower()
    drug=re.search(r'\b(drug(a|u|om|ovi|ove|ovima)?|druze|drugaric(a|e|i|om|ama))\b',text_withoutdia)
    prijatelj=re.search(r'\b(prijatelj(a|u|em|e|ima)?|prijateljic(a|u|e|i|om|ama))\b', text_withoutdia)
    if drug:
        return "drug"
    elif prijatelj:
        return "prijatelj"
    else:
        return "NA"


#---End Lexical Features -----------------------------------------------------------------------------------------------

#---Start Morpho-Synt. Features ----------------------------------------------------------------------------------------

# – infinitive without ”i”

def inf_without_i(text):
  text_withoutdia = remove_diacritics(text).lower()
  distr_no_i,distr_i={},{}
  for token in tokenize(text_withoutdia):
      if token.endswith(u"c") or token.endswith(u"t"):
          mod_token = token+u"i"
          if mod_token in inf_dict:
              distr_no_i[mod_token]=1
      elif token.endswith(u"ci") or token.endswith(u"ti"):
          if token in inf_dict:
              distr_i[token]=1
  if len(distr_no_i)!=0 and len(distr_i)!=0:
      return "both inf with and inf without i"
  elif len(distr_no_i)!=0 and len(distr_i)==0:
    return "inf without i"
  elif len(distr_no_i)==0 and len(distr_i)!=1:
    return "inf with i"
  else:
    return "NA"

#– synthetic future tense
#syntinfverbs

def synt_future(text):
  distrsynt, distrnosynt = {},{}
  text_withoutdia = remove_diacritics(text).lower()
  syntend_re=re.search(ur'\s(\w+(cu|ces|ce|cemo|cete|ce))\s',text_withoutdia, re.UNICODE)
  nosyntend_re=re.search(ur'\s(\w+(t|c)) (cu|ces|ce|cemo|cete|ce)\s',text_withoutdia, re.UNICODE)
  if syntend_re:
      if syntend_re.group(1) in syntinf_dict:
          distrsynt[syntend_re.group(1)]=1
  elif nosyntend_re:
      if nosyntend_re.group(1) in inf_dict or nosyntend_re.group(1)+u"i" in inf_dict:
          distrnosynt[nosyntend_re.group(1)]=1
  if len(distrsynt)==1 and len(distrnosynt)==1:
      return "both synt & nosynt inf"
  elif len(distrsynt)==1:
    return "synt inf"
  elif len(distrnosynt)==1:
    return "nosynt inf"
  else:
    return "NA"

def da(text):
    if "da" in tokenize(text.lower()):
        return "da"
    else:
        return "NA"

def da_present(text):
    ## TODO COUNT
    text_withoutdia = remove_diacritics(text).lower()
    if "da" in tokenize(text_withoutdia)[1:-2]:
        dasent = tokenize(text_withoutdia)
        ## if we want to add a condition before "da"
        #if #dasent[dasent.index("da")-1] in presverbs/modalverbs and
        if dasent[dasent.index("da")+2] in presverbs:
            return "da pres"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        elif dasent[dasent.index("da")+2] not in presverbs:
            return "da no pres"
        else:
            return "NA"
    elif "da" in tokenize(text_withoutdia)[1:-1]:
        dasent = tokenize(text_withoutdia)
        ## if we want to add a condition before "da"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        if  dasent[dasent.index("da")+1] in presverbs:
            return "da pres"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        elif  dasent[dasent.index("da")+1] not in presverbs:
            return "da no pres"
        else:
            return "NA"
    else:
        return "NA"


def genitiva(text):
    # TODO nekog/onog/tog ?
    # TODO #ome, om ?
    text_withoutdia = remove_diacritics(text).lower()
    oga_re=re.search(ur'\b(\w+oga)\b',text_withoutdia, re.UNICODE)
    og_re=re.search(ur'\b(\w+og)\b',text_withoutdia, re.UNICODE)
    if oga_re:
        if oga_re.group(1)[:-1] in genitiv_og_dict:
            return "oga"
        else:
            return "NA"
    elif og_re:
        if og_re.group(1) in genitiv_og_dict:
            return "og"
        else:
            return "NA"
    else:
        return "NA"

def ir_ov_is(text):
    text_withoutdia = remove_diacritics(text).lower()
    ir=re.search(ur'\b(\w{3,})(iram|iras|ira|iramo|irate|iraju|irala|iralo|irali|irale)\b',text_withoutdia, re.UNICODE)
    ov=re.search(ur'\b(\w{3,})(ujem|ujes|uje|ujemo|ujete|uju|ovao|ovala|ovalo|ovali|ovale)\b',text_withoutdia, re.UNICODE)
    isa=re.search(ur'\b(\w{3,})(isem|ises|ise|isemo|isete|isu|isao|isala|isalo|isali|isale)\b',text_withoutdia, re.UNICODE)
    if ir:
        if ir.group(1) in stems_dict:
            return "irati"
        else:
            return "NA"
    elif ov:
        if ov.group(1) in stems_dict:
            return "ovati"
        else:
            return "NA"
    elif isa:
        if isa.group(1) in stems_dict:
            return "isati"
        else:
            return "NA"
    else:
        return "NA"

def inf_verb_ratio(text):
    nr_verbs = 0
    nr_inf = 0
    for token in tokenize(remove_diacritics(text).lower()):
        if token in verbs_dict:
            nr_verbs+=1
            if token in inf_dict:
                nr_inf+=1
    if nr_verbs>0:
        return round(nr_inf/nr_verbs,2)
    else:
        return "NA"


#---End Morpho-Synt. Features ------------------------------------------------------------------------------------------


def cyrillic(text):
    """""Check if cyrillic letters in text"""""

    #retruns many other characters (Russian) too
    serbian_alphabet_cyrillic = u'АаБбВвГгДдЂђЕеЖжЗзИиЈјКкЛлЉљМмНнЊњОоПпРрСсТтЋћУуФфХхЦцЧчЏџШш'
    cyril = re.findall(u"[\u0400-\u0500]+", text)
    not_sr_cyril = []
    sr_cyril = []
    for word in cyril:
        for letter in word:
            if letter not in serbian_alphabet_cyrillic:
                not_sr_cyril.append(letter)
            else:
                sr_cyril.append(letter)
    if len(not_sr_cyril) > 0:
        return "Mix Cyrillic"
    elif len(sr_cyril)>0:
        return "SR Cyrilic"
    else:
        return "Latin"

t="\t"
out=gzip.open('hrsrTweets.var.gz','w')
out.write(t+t+t+t+t+t+t+"text metainformation"+t+"yat"+t+"k (hr) vs. h (sr)"+t+"h-drop"+t+"r (hr) vs. r-drop(sr)"+t
              +"č & ć deviation"+t+"št (sr) vs. ć (hr)"+t+"eu/au (hr) vs. ev/av (sr)"+t
              +"sa & s deviation"+t+"tko vs. ko" +t+"šta vs. što"+t+"da li vs. je li"+t
              +"usprkos/uprkos/unatoč"+t+"bre/bolan/bona/ba"+t+"mnogo/puno/vrlo/jako"+t+"hr mjeseci vs. intern. mjeseci"+t+"tjedan/nedjelja/nedelja/sedmica"+t+"drug/prijatelj (m/f)"+t
              +"treba da vs. trebaXXX da"+t+"inf with/without -i"+t+"synt. future"+t+"'da' in text"+t
              +"da+present"+t+"genitiv og/oga"+t+"irati/ovati/isati"+t+"inf/verb ratio"+t
              +"'-ist'(hr) vs. '-ista' (sr)"+t+"Cyrillic/Latin"+"\n")

## Left out +ao_o(text)

for line in gzip.open('hrsrTweets.gz'):
    tid,user,time,lang,lon,lat,text=line[:-1].decode('utf8').split('\t')
    out.write(line[:-1]+t+clean(text,lang)+t+yat(text)+t+kh(text)+t+hdrop(text)+t+rdrop(text)+t
             +c_ch(text)+t+st(text)+t+diftong(text)+t
             +sa_s(text)+t+tko_ko(text)+t+sta_sto(text)+t+da_je_li(text)+t
             +usprkos(text)+t+bre(text)+t+mnogo(text)+t+months(text)+t+tjedan(text)+t+drug(text)+t
             +treba_da(text)+t+inf_without_i(text)+t+synt_future(text)+t+da(text)+t
             +da_present(text)+t+genitiva(text)+t+ir_ov_is(text)+t+str(inf_verb_ratio(text))+t
             +ist(text)+t+cyrillic(text)+"\n")
out.close()
