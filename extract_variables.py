#!/usr/bin/python
#-*-coding:utf8-*-

## Script for annotating the presence or absence of variables in the tweet corpus
## The considered features are of phonetical, lexical and morpho-syntactical nature
## The output file hrsrTweets.var.gz contains the tweets, their metadata and values for each feature (tab separated)

from __future__ import division
import gzip
import re


dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

token_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+|\w+',re.UNICODE)
yat_lexicon=dict([e[:-1].split('\t') for e in gzip.open('custom-lexicons/yat-lexicon.gz')])
kh_lexicon=dict([k[:-1].split('\t') for k in gzip.open('custom-lexicons/kh-lexicon.gz')])
hdrop_lexicon=dict([h[:-1].split('\t') for h in gzip.open('custom-lexicons/hdrop-lexicon.gz')])
rdrop_lexicon=dict([r[:-1].split('\t') for r in gzip.open('custom-lexicons/rdrop-lexicon.gz')])
ir_is_dict=dict([iris[:-1].split('\t') for iris in gzip.open('custom-lexicons/ir-is-lexicon.gz')])
ir_ov_dict=dict([irov[:-1].split('\t') for irov in gzip.open('custom-lexicons/ir-ov-lexicon.gz')])
st_c_lexicon=dict([st[:-1].split('\t') for st in gzip.open('custom-lexicons/st-c-lexicon.gz')])
diftong_lexicon=dict([diftong[:-1].split('\t') for diftong in gzip.open('custom-lexicons/diftong-v-lexicon.gz')])
ch_dict={ch.rstrip("\n").decode("utf8"):1 for ch in gzip.open('custom-lexicons/ch-lexicon.gz')}
inf_dict={inf.rstrip("\n").decode("utf8"):1 for inf in gzip.open('custom-lexicons/verbs-inf-lexicon.gz')}
syntinf_dict={syntinf.rstrip("\n").decode("utf8"):1 for syntinf in gzip.open('custom-lexicons/verbs-vmf-lexicon.gz')}
verbs_dict={verb.rstrip("\n").decode("utf8"):1 for verb in gzip.open('custom-lexicons/verbs-lexicon.gz')}
presverbs={pres.rstrip("\n").decode("utf8"):1 for pres in gzip.open('custom-lexicons/verbs-pres-lexicon.gz')}
genitiv_og_dict={genitiv_og.rstrip("\n").decode("utf8"):1 for genitiv_og in gzip.open('custom-lexicons/genitiv-og-eg-lexicon.gz')}
intmonths={x.rstrip("\n").decode("utf8"):1 for x in gzip.open('custom-lexicons/int-months.gz')}
hrmonths={x.rstrip("\n").decode("utf8"):1 for x in gzip.open('custom-lexicons/hr-months.gz')}
#ist_dict={ist.rstrip("\n"):1 for ist in gzip.open('custom-lexicons/ist.gz')}




def tokenize(text):
  return token_re.findall(text)


##---Start Cleanining Features------------------------------------------------------------------------------------------


def clean(text,lang):
    automatic_re = re.search("(tweep|automatically checked by|Objavio/la sam novu fotografiju|Just posted a photo|Today stats:"
                             "|I just ousted|I'm at|I (just)? ?(voted|added)|via (Tumblr|Facebook)"
                             "|I liked a @YouTube)",text)
    if automatic_re: #or "tweep" in text in "automatically checked by" in text:
        return "automatic"
    # if you want to be 100% sure
    #elif lang.startswith("en:1"):
    #     return "English tweet"
    # otherwise just eliminate other aproximations
    elif lang.startswith("en:") or ("if you" in text or " visit " in text):
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
            ## other_non_bkms_tweets_re = re.search("\w+? ?(Follow me on|check (this)? ?out|you should|untitled)",text)
            #if other_non_bkms_tweets_re:
             #   return "other"


##--- End Cleanining Features-------------------------------------------------------------------------------------------

#---Start Phonetical Features-------------------------------------------------------------------------------------------

## TODO MAKE BOTH FOR ALL FEATURES

def yat(text):
  """returns "e" if ekavica and "je" if (i)jekavica, NA if none """
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in yat_lexicon:
      distr[yat_lexicon[token]]=distr.get(yat_lexicon[token],0)+1
  #if there are not yat-reflexes in the sentence
  if len(distr)==0:
    return 'NA'
  # if there are both reflexes
  elif len(distr)==2:
    #sdistr=sorted(distr.items(),key=lambda x:-x[1])
    #if sdistr[0][1]==sdistr[1][1]:
        #return 'NA'
    return "both"
        # eg. zasto novosadjani pricaju o mestu skoci djevojka zivim ovde 15 godina nikad nisam cula za to e
    #else:
     #   return sdistr[0][0]
  else:
    return distr.keys()[0]

def kh(text):
  """returns k if initial k instead of h (croatian) and h if initial h instead of k (serbian)
   variation of the same word (ex. kemija/hemija), NA if none   """
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in kh_lexicon:
      distr[kh_lexicon[token]]=distr.get(kh_lexicon[token],0)+1
  if len(distr)==0: #or len(distr)==2:
    return 'NA'
  elif len(distr)==2:
      return "both"
  else:
    return distr.keys()[0]

def hdrop(text):
  """returns h if initial "h" is not dropped and "h_drop" if it is dropped (ex. historija/istorija), NA if none """
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in hdrop_lexicon:
      distr[hdrop_lexicon[token]]=distr.get(hdrop_lexicon[token],0)+1
  if len(distr)==0: #or len(distr)==2:
    return 'NA'
  elif len(distr)==2:
      return "both"
  else:
    return distr.keys()[0]

def rdrop(text):
  """returns r if "r" is not dropped and "r_drop" if it is dropped (ex. jucer/juce), NA if none """
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in rdrop_lexicon:
      distr[rdrop_lexicon[token]]=distr.get(rdrop_lexicon[token],0)+1
  if len(distr)==0: #or len(distr)==2:
    return 'NA'
  elif len(distr)==2:
      return "both"
  else:
    return distr.keys()[0]

def st_c(text):
  """returns "ć" if "ć"-sequence (croatian) instead of "št"-sequence (serbian) and the other way around (uopće/uopšte),
  NA if none"""
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in st_c_lexicon:
      distr[st_c_lexicon[token]]=distr.get(st_c_lexicon[token],0)+1
  if len(distr)==0 or len(distr)==2:
    return 'NA'
  else:
    return distr.keys()[0]

def diftong(text):
  """returns eu/au if croatian diphtong or ev/av if serbian variation (euro/evro, august/avgust), NA if none"""
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in diftong_lexicon:
      distr[diftong_lexicon[token]]=distr.get(diftong_lexicon[token],0)+1
  if len(distr)==0:
      return 'NA'
  elif len(distr)==2:
      return "both"
  else:
      return distr.keys()[0]




def c_ch(text):
    distr_ch,distr_c={},{}
    for token in tokenize(text.lower()):
        if u"ć" in token and token not in ch_dict:
            ## if it's not an infinitiv without -i (reć)
            if not (token.endswith(u"ć") and token+"i" in inf_dict):
                mod_token = token.replace(u"ć", u"č")
                if mod_token in ch_dict:
                ## exception (to add in SR lexicons)
                    if not token in [u"kaće", u"deće"]:
                        distr_ch[mod_token]=1
        if u"č" in token and token not in ch_dict:
            mod_token = token.replace(u"č", u"ć")
            if mod_token in ch_dict:
                distr_c[mod_token]=1

    if len(distr_ch)>0 and len(distr_c)>0:
        return "both"
    if len(distr_ch)>0:
        return "č dev"
    elif len(distr_c)>0:
        return "ć dev"
    else:
        return "NA"

def sa_s(text):

    """ returns "sa dev" if sa-rule deviation and "s dev" if s-rule deviation, "both" if both and "NA" if none
    http://savjetnik.ihjj.hr/savjet.php?id=17
    Prijedlog sa upotrebljava se samo ispred riječi koje počinju glasovima s, š, z, ž
    other (more complicated) source http://jezicna-pomoc.lss.hr/jsavjeti.php?view=2"""

    text = text.lower()
    s_re_dev=re.search(r'\bs\s((s|z|š|ž)|(?!aeiou)(s|z|š|ž))',text)
    sa_re_dev=re.search(r'\bsa\s(?!((s|z|š|ž)|(?!aeiou)(s|z|š|ž)|mnom))',text)
    if s_re_dev and sa_re_dev:
        return "both"
    if s_re_dev:
        return "s dev"
    elif sa_re_dev:
        return "sa dev"
    else:
        return "NA"


#---End Phonetical Features---------------------------------------------------------------------------------------------

#---Start Lexical Features----------------------------------------------------------------------------------------------



def tko_ko(text):
    """ returns "tko" if tko (and other pronuns with tk) and "ko" if "ko" (and other pronuns with ko),
     "both" if both and "NA" if none """
    text_withoutdia = remove_diacritics(text).lower()
    tko_re=re.search(r'\b(ne|gdje|ni|i|sva|koje)?tko\b',text_withoutdia)
    ko_re=re.search(r'\b(ne|ni|i|sva|koje)?ko\b',text_withoutdia)

    if tko_re and ko_re:
        return "both"
    elif tko_re:
        return "tko"
    elif ko_re:
        return "ko"
    else:
        return "NA"

def sta_sto(text):
    """ returns "što" if "sto" in tweet and "šta" if "sta" in tweet
     "both" if both and "NA" if none """
    ## Problems:
    ## - što interrogative meaning same for all languages:  Sto da ne
    ## - sto without diacritics = 100
    text_withoutdia = remove_diacritics(text).lower()
    sto_re=re.search(r'\b(sto)\b',text_withoutdia)
    sta_re=re.search(r'\b(sta)\b',text_withoutdia)
    if sto_re and sta_re:
        return "both"
    elif sto_re:
        return 'što'
    elif sta_re:
        return 'šta'
    else:
        return 'NA'

def da_je_li(text):
    """returns "da li" if "da li" in tweet and "je li" if "je li" in tweet
     "both" if both and "NA" if none"""
    text_withoutdia = remove_diacritics(text).lower()
    dali_re=re.search(r'\b(da li|dal)\b',text_withoutdia)
    jeli_re=re.search(r'\b(je li|jel)\b',text_withoutdia)
    if dali_re and jeli_re:
        return "both"
    elif dali_re:
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
    """returns "treba da" if "treba da" in tweet and "trebaX da" if treba\w+\sda in tweet (ex. trebam da)
     "both" if both and "NA" if none"""
    """" treba da vs. treba* da """""
    text_withoutdia = remove_diacritics(text).lower()
    trebada=re.search(r'\b(treba|trebalo je|trebalo bi)\sda\b',text_withoutdia, re.UNICODE)
    trebaXsg=re.search(r'\btreba(m|s|mo|te|ju)\sda\b',text_withoutdia, re.UNICODE)
    trebaXpl=re.search(r'\btreba(la|o|li|le)\s(sam|si|je|smo|ste|su|bi)\sda\b',text_withoutdia, re.UNICODE)

    if trebada and (trebaXsg or trebaXpl):
        return "both"
    elif trebada:
        return "treba da"
    elif trebaXsg or trebaXpl:
        return "trebaX da"
    else:
        return "NA"


def bre(text):
    """ returns  bre, bolan, ba or NA, depending on the presence of thise stings in tweets """
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
    #TODO check if it makes sense
    text_withoutdia = remove_diacritics(text).lower()
    mnogo=re.search(r'\bmnogo\b',text_withoutdia, re.UNICODE)
    puno=re.search(r'\bpuno\b',text_withoutdia, re.UNICODE)
    vrlo=re.search(r'\bvrlo\b',text_withoutdia, re.UNICODE)
    jako=re.search(r'\bjako\b',text_withoutdia, re.UNICODE)

    if mnogo:
        return 'mnogo'
    elif puno:
        return 'puno'
    elif vrlo:
        return 'vrlo'
    elif jako:
        return 'jako'
    else:
        return "NA"

def months(text):
    """returns "HR months" if croatian month names and "international months" if international, both if both and NA if none  """
    text_withoutdia = remove_diacritics(text).lower()
    hr,international = 0,0
    for token in tokenize(text_withoutdia):
        if token in hrmonths:
            hr+=1
        elif token in intmonths:
            international+=1
    if hr>0 and international>0:
        return "both"
    elif hr>0:
        return "HR months"
    elif international>0:
        return "international months"
    else:
        return "NA"

def tjedan(text):
    """returns tjedan/sedmica/nedjelja/nedelja/NA """
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
    """returns drug/prijatelj/both/NA"""
    #TODO: include variations such as drugaricin, drugarski etc?
    text_withoutdia = remove_diacritics(text).lower()
    drug=re.search(r'\b(drug(a|u|om|ovi|ove|ovima)?|druze|drugaric(a|e|i|om|ama))\b',text_withoutdia)
    prijatelj=re.search(r'\b(prijatelj(a|u|em|e|ima)?|prijateljic(a|u|e|i|om|ama))\b', text_withoutdia)
    if drug and prijatelj:
        return "both"
    elif drug:
        return "drug"
    elif prijatelj:
        return "prijatelj"
    else:
        return "NA"


#---End Lexical Features -----------------------------------------------------------------------------------------------

#---Start Morpho-Synt. Features ----------------------------------------------------------------------------------------

# – infinitive without ”i”

def inf_without_i(text):
  """return "inf without i" if infinitiv without -i ending and "inf with i" if infinitiv with -i ending,
   both if both and NA if none"""
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
  if len(distr_no_i)>0 and len(distr_i)>0:
      return "both"
  elif len(distr_no_i)>0:
    return "inf without i"
  elif len(distr_i)>0:
    return "inf with i"
  else:
    return "NA"

#– synthetic future tense
#syntinfverbs

def synt_future(text):
  """return "synt inf" if syntetic infinitiv (uradicu), "nosynt inf" if analytic infinitiv (uradit cu),
  "both" if both and NA if none """
  distrsynt, distrnosynt = {},{}
  text_withoutdia = remove_diacritics(text).lower()
  syntend_re=re.search(ur'\b(\w+)(cu|ces|ce|cemo|cete|ce)\b',text_withoutdia, re.UNICODE)
  nosyntend_re=re.search(ur'\b(\w+(t|c)) (cu|ces|ce|cemo|cete|ce)\b',text_withoutdia, re.UNICODE)
  if syntend_re:
      if syntend_re.group() in syntinf_dict:
          distrsynt[syntend_re.group()]=1
  elif nosyntend_re:
      if nosyntend_re.group(1) in inf_dict or nosyntend_re.group(1)+u"i" in inf_dict:
          distrnosynt[nosyntend_re.group(1)]=1
  if len(distrsynt)>0 and len(distrnosynt)>0:
      return "both"
  elif len(distrsynt)>0:
    return "synt inf"
  elif len(distrnosynt)>0:
    return "nosynt inf"
  else:
    return "NA"

def da(text):
    """return "da" if da in text and NA if not"""
    if "da" in tokenize(text.lower()):
        return "da"
    else:
        return "NA"



def da_present(text):
    """"return "da pres" if "da" is followed by verb in present tense in the +2 window,
      "da without pres" if it is not, and NA if there is no "da" in the tweet  """
    ## TODO solve problem ---bla bla da ces----
    text_withoutdia = remove_diacritics(text).lower()
    if "da" in tokenize(text_withoutdia)[1:-2]:
        dasent = tokenize(text_withoutdia)
        ## if we want to add a condition before "da"
        #if #dasent[dasent.index("da")-1] in presverbs/modalverbs and
        if dasent[dasent.index("da")+2] in presverbs:
            #print dasent[dasent.index("da")+2], type(dasent[dasent.index("da")+2])
            return "da pres"
        else:
            return "NA"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        #elif dasent[dasent.index("da")+2] not in presverbs:
         #   return "da without pres"
        #else:
         #   return "NA"
    if "da" in tokenize(text_withoutdia)[1:-1]:
        dasent = tokenize(text_withoutdia)
        ## if we want to add a condition before "da"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        if  dasent[dasent.index("da")+1] in presverbs:
            return "da pres"
        else:
            return "NA"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        #elif  dasent[dasent.index("da")+1] not in presverbs:
        #    return "da without pres"
        #else:
        #    return "NA"
    else:
        return "NA"


def genitiva(text):
    """return "oga" if a word in tweet is ending with -oga and is in the list of genitiv-(o|e)g/a endings
      "og/eg" if a word in tweet is ending with -og/eg and is in the list of genitiv-og/a endings,
       both if both and NA if none"""
    # TODO decide whether to do the same for -ome, -om
    text_withoutdia = remove_diacritics(text).lower()
    oga_re=re.search(ur'\b(\w+(o|e)ga)\b',text_withoutdia, re.UNICODE)
    og_re=re.search(ur'\b(\w+(o|e)g)\b',text_withoutdia, re.UNICODE)
    if og_re and oga_re:
    #    return "both"
        if oga_re.group(1)[:-1] in genitiv_og_dict and og_re.group(1) in genitiv_og_dict:
            return "both"
        else:
            return "NA"
    elif oga_re:
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

def ir_is(text):
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in ir_is_dict:
      distr[ir_is_dict[token]]=distr.get(ir_is_dict[token],0)+1
  if len(distr)==0: #or len(distr)==2:
    return 'NA'
  elif len(distr)==2:
      return "both"
  else:
    return distr.keys()[0]


def ir_ov(text):
  distr={}
  for token in tokenize(remove_diacritics(text).lower()):
    if token in ir_ov_dict:
      distr[ir_ov_dict[token]]=distr.get(ir_ov_dict[token],0)+1
  if len(distr)==0: #or len(distr)==2:
    return 'NA'
  elif len(distr)==2:
      return "both"
  else:
    return distr.keys()[0]


def inf_verb_ratio(text):
    """return ratio nr.infinitiv/nr.allverbs """
    # TODO: if uradicu infinitiv
    nr_verbs = 0
    nr_inf = 0
    for token in tokenize(remove_diacritics(text).lower()):
        if token in verbs_dict:
            nr_verbs+=1
            if (token in inf_dict) or (token in syntinf_dict):
                nr_inf+=1
    if nr_verbs>0:
        return round(nr_inf/nr_verbs,2)
    else:
        return "NA"


#---End Morpho-Synt. Features ------------------------------------------------------------------------------------------


def cyrillic(text):
    """Check if cyrillic letters in text"""
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

    if len(sr_cyril)>len(not_sr_cyril):
       return "sr cyrillic"
    elif len(not_sr_cyril)>len(sr_cyril):
       return "mix cyrillic"
    else:
       return "latin"

t="\t"

out=gzip.open('hrsrTweets.var.gz','w')
out.write(t+t+t+t+t+t+t+"text metainformation"+t+"yat"+t+"k (hr) vs. h (sr)"+t+"h-drop"+t+"r (hr) vs. r-drop(sr)"+t
              +"št (sr) vs. ć (hr)"+t+"č & ć deviation"+t+"eu/au (hr) vs. ev/av (sr)"+t
              +"sa & s deviation"+t+"tko vs. ko" +t+"šta vs. što"+t+"da li vs. je li"+t
              +"usprkos/uprkos/unatoč"+t+"bre/bolan/bona/ba"+t+"mnogo/puno/vrlo/jako"+t
              +"hr mjeseci vs. intern. mjeseci"+t+"tjedan/nedjelja/nedelja/sedmica"+t
              +"drug/prijatelj (m/f)"+t+"treba da vs. trebaXXX da"+t
              +"inf with/without -i"+t+"synt. future"+t+"'da' in text"+t
              +"da+present"+t+"genitiv og/oga"+t+"irati/isati"+t
              +"irati/ovati"+t+"inf/verb ratio"+t
              +"Cyrillic/Latin"+"\n")

# ## Left out +ao_o(text)
# ## Left out +ist(text)
#
for line in gzip.open('hrsrTweets.gz'):
    tid,user,time,lang,lon,lat,text=line[:-1].decode('utf8').split('\t')
    out.write(line[:-1]+t+clean(text,lang)+t+yat(text)+t+kh(text)+t+hdrop(text)+t+rdrop(text)+t
             +st_c(text)+t+c_ch(text)+t+diftong(text)+t
             +sa_s(text)+t+tko_ko(text)+t+sta_sto(text)+t+da_je_li(text)+t
             +usprkos(text)+t+bre(text)+t+mnogo(text)+t
             +months(text)+t+tjedan(text)+t
             +drug(text)+t+treba_da(text)+t
             +inf_without_i(text)+t+synt_future(text)+t+da(text)+t
             +da_present(text)+t+genitiva(text)+t+ir_is(text)+t
             +ir_ov(text)+t+str(inf_verb_ratio(text))+t
             +cyrillic(text)+"\n")
out.close()

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


# #vizazist/vizazista (false positivs alert: it always can be a genitiv)
# def ist(text):
#     distr_ist,distr_ista={},{}
#     for token in tokenize(remove_diacritics(text).lower()):
#         if token.endswith("ista"):
#             if token[:-1] in ist_dict:
#                 distr_ista[token]=1
#         elif token.endswith("ist"):
#             if token in ist_dict:
#                 distr_ist[token]=1
#     if len(distr_ist)==1:
#         return "ist"
#     elif len(distr_ista)==1:
#         return "ista"
#     else:
#         return "NA"