#!/usr/bin/python
#-*-coding:utf8-*-

## Script for annotating the presence or absence of variables in the tweet corpus
## The considered features are of phonetical, lexical and morpho-syntactical nature
## The output file hrsrTweets.var.gz contains the tweets, their metadata and values for each feature (tab separated)

from __future__ import division
import gzip
import re

t="\t"
dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}

def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

token_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+|\w+',re.UNICODE)
yat_lexicon=dict([e[:-1].decode("utf8").split('\t') for e in gzip.open('custom-lexicons/yat-lexicon.gz')])
kh_lexicon=dict([k[:-1].decode("utf8").split('\t') for k in gzip.open('custom-lexicons/kh-lexicon.gz')])
hdrop_lexicon=dict([h[:-1].decode("utf8").split('\t') for h in gzip.open('custom-lexicons/hdrop-lexicon.gz')])
rdrop_lexicon=dict([r[:-1].decode("utf8").split('\t') for r in gzip.open('custom-lexicons/rdrop-lexicon.gz')])
ir_is_dict=dict([iris[:-1].decode("utf8").split('\t') for iris in gzip.open('custom-lexicons/ir-is-lexicon.gz')])
ir_ov_dict=dict([irov[:-1].decode("utf8").split('\t') for irov in gzip.open('custom-lexicons/ir-ov-lexicon.gz')])
st_c_lexicon=dict([st[:-1].decode("utf8").split('\t') for st in gzip.open('custom-lexicons/st-c-lexicon.gz')])
diftong_lexicon=dict([diftong[:-1].decode("utf8").split('\t') for diftong in gzip.open('custom-lexicons/diftong-v-lexicon.gz')])
ch_dict={ch.rstrip("\n").decode("utf8"):1 for ch in gzip.open('custom-lexicons/ch-lexicon.gz')}
inf_dict={inf.rstrip("\n").decode("utf8"):1 for inf in gzip.open('custom-lexicons/verbs-inf-lexicon.gz')}
synt_futur_dict={syntinf.rstrip("\n").decode("utf8"):1 for syntinf in gzip.open('custom-lexicons/verbs-vmf-lexicon.gz')}
verbs_dict={verb.rstrip("\n").decode("utf8"):1 for verb in gzip.open('custom-lexicons/verbs-lexicon.gz')}
presverbs={pres.rstrip("\n").decode("utf8"):1 for pres in gzip.open('custom-lexicons/verbs-pres-lexicon.gz')}
modalverbs={pres.rstrip("\n").decode("utf8"):1 for pres in gzip.open('custom-lexicons/modalverbs-lexicon.gz')}
genitiv_og_dict={genitiv_og.rstrip("\n").decode("utf8"):1 for genitiv_og in gzip.open('custom-lexicons/genitiv-og-eg-lexicon.gz')}
intmonths={x.rstrip("\n").decode("utf8"):1 for x in gzip.open('custom-lexicons/int-months.gz')}
hrmonths={x.rstrip("\n").decode("utf8"):1 for x in gzip.open('custom-lexicons/hr-months.gz')}

# dog={x.rstrip("\n").decode("utf8"):1 for x in gzip.open('custom-lexicons/dogoditi-dogadjati.gz')}
# des={x.rstrip("\n").decode("utf8"):1 for x in gzip.open('custom-lexicons/desiti-desavati.gz')}



def tokenize(text):
  return token_re.findall(text)


def check_var_in_tab_sep_lexicons(text, mylex):
  distr={}
  for token in tokenize(text.lower()):
    if token in mylex:
      distr[mylex[token]]=distr.get(mylex[token],[])+[token]
  if len(distr)==0:
      return u'NA'
  elif len(distr)==2:
      return (u"both", distr.values()[0]+distr.values()[1])
  else:
      return (distr.keys()[0], distr.values()[0])



##---Start Cleanining Features------------------------------------------------------------------------------------------


def clean(text,lang):
    automatic_re = re.search("(tweep|automatically checked by|Objavio/la sam novu fotografiju|Just posted a photo|Today stats:"
                             "|I just ousted|I'm at|I (just)? ?(voted|added)|via (Tumblr|Facebook)"
                             "|I liked a @YouTube)",text)
    if automatic_re: #or "tweep" in text in "automatically checked by" in text:
        return "automatic"
    # if you want to be 100% sure that the tweet is english:
    elif lang.startswith("en:1") or ("if you" in text or " visit " in text):
         return "en tweet"
    else:
        if len(tokenize(text))==2:
             emoji_punct_website_re = re.search("^[^A-Za-z]+ ?http.+$",text,re.UNICODE)
             user_website_re = re.search("^@.+ ?http.+$",text,re.UNICODE)
             user_puncta = re.search("^@.+ ?[^A-Za-z]+$",text,re.UNICODE)
             user_punctb = re.search("[^A-Za-z]+ ?@.+?$",text,re.UNICODE)
             if emoji_punct_website_re or user_website_re:
                 return u"website noise"
             elif user_puncta or user_punctb:
                 return u"user noise"
             else:
                 return u"NA"
        elif len(tokenize(text)) == 1:
            only_punct_re = re.search("^[^A-Za-z]+$",text,re.UNICODE)
            if "".join(tokenize(text)).startswith("http"):
                return u"website"
            elif only_punct_re:
                return u"not alpha"
            else:
                return u"NA"
        else:
            return u"NA"



##--- End Cleanining Features-------------------------------------------------------------------------------------------

#---Start Phonetical Features-------------------------------------------------------------------------------------------

## TODO MAKE BOTH FOR ALL FEATURES

def yat(text):
  """returns "e" if ekavica and "je" if (i)jekavica, NA if none """

  # TODO: recognize vidjecemo vs videcemo
  myyat=check_var_in_tab_sep_lexicons(text,yat_lexicon)
  return myyat

def kh(text):
    mykh=check_var_in_tab_sep_lexicons(text,kh_lexicon)
    return mykh
  # """returns k if initial k instead of h (croatian) and h if initial h instead of k (serbian)
  #  variation of the same word (ex. kemija/hemija), NA if none   """

def hdrop(text):
#  """returns h if initial "h" is not dropped and "h_drop" if it is dropped (ex. historija/istorija), NA if none """
    myhdrop=check_var_in_tab_sep_lexicons(text,hdrop_lexicon)
    return myhdrop

def rdrop(text):
    myrdrop=check_var_in_tab_sep_lexicons(text,rdrop_lexicon)
    return myrdrop
 # """returns r if "r" is not dropped and "r_drop" if it is dropped (ex. jucer/juce), NA if none """

def st_c(text):
    myst_c=check_var_in_tab_sep_lexicons(text,st_c_lexicon)
    return myst_c
  # """returns "ć" if "ć"-sequence (croatian) instead of "št"-sequence (serbian) and the other way around (uopće/uopšte),

def diftong(text):
    mydiftong=check_var_in_tab_sep_lexicons(text,diftong_lexicon)
    return mydiftong
  # """returns eu/au if croatian diphtong or ev/av if serbian variation (euro/evro, august/avgust), NA if none"""

#
def c_ch(text):
    distr_dev_ch,distr_dev_c=[],[]
    for token in tokenize(text.lower()):
        if u"ć" in token:
            if token not in ch_dict:
            ## if it's not an infinitiv without -i (reć)
                if not (token.endswith(u"ć") and token+u"i" in inf_dict):
                    mod_token = token.replace(u"ć", u"č")
                    if mod_token in ch_dict:
                    ## exception (to add in SR lexicons)
                        if not token in [u"kaće", u"deće"]:
                            distr_dev_ch.append(mod_token)
        if u"č" in token:
            if token not in ch_dict:
                mod_token = token.replace(u"č", u"ć")
                if mod_token in ch_dict:
                    distr_dev_c.append(mod_token)

    if len(distr_dev_ch)>0 and len(distr_dev_c)>0:
        return (u"both", distr_dev_ch+distr_dev_c)
    if len(distr_dev_ch)>0:
        return (u"ch-dev", distr_dev_ch)
    elif len(distr_dev_c)>0:
        return (u"c-dev",distr_dev_c)
    else:
        return u"NA"
#
#
#
def sa_s(text):

    """ returns "sa dev" if sa-rule deviation and "s dev" if s-rule deviation, "both" if both and "NA" if none
    http://savjetnik.ihjj.hr/savjet.php?id=17
    Prijedlog sa upotrebljava se samo ispred riječi koje počinju glasovima s, š, z, ž
    other (more complicated) source http://jezicna-pomoc.lss.hr/jsavjeti.php?view=2"""

    text = text.lower()
    s_re_dev = re.findall(ur'\bs\s[szšž]\w+?\b', text, re.UNICODE)
    sa_re_dev=re.findall(ur'\bsa\s[^szšž]\w+?\b',text, re.UNICODE)
    sa_mnom=re.findall(ur'\bsa mnom\b',text, re.UNICODE)

    if s_re_dev and sa_re_dev:
        return (u"both", s_re_dev+sa_re_dev)
    if s_re_dev:
        return (u"s-dev",s_re_dev)
    elif sa_re_dev and (sa_mnom !=sa_re_dev):
        return (u"sa-dev",sa_re_dev)
    else:
        return u"NA"


# #---End Phonetical Features---------------------------------------------------------------------------------------------
#
# #---Start Lexical Features----------------------------------------------------------------------------------------------
#
#
#
def tko_ko(text):
    """ returns 'tko' if tko  and 'ko' if 'ko'"""
    # TODO
    # if next token == VERB
    # if not previous token == VERB
    # if not next token == PER (ja, ti, on, ona, mi, vi, oni)
    # if not next token == NER
    # if not next token == NOUN in Nominativ
    # ko + mene, me, te, tebe, njega, ga, nju, ju, nas, vas, ih
    # ko + ne
    tok = tokenize(text.lower())
    if u"tko" in tok and u"ko" in tok:
        return (u"both", [u"tko", u"ko"])
    elif u"tko" in tok:
        return (u"tko",[u"tko"])
    elif u"ko" in tok:
        return (u"ko",[u"ko"])
    else:
        return u"NA"
#
def sta_sto(text):
    """ returns "što" if "sto" in tweet and "šta" if "sta" in tweet
     "both" if both and "NA" if none """
    ## Problems:
    ## - što interrogative meaning same for all languages:  Sto da ne
    ## - sto without diacritics = 100
    tok = tokenize(text.lower())
    if (u"sto" or u"što") in tok and (u"sta" or u"šta") in tok:
        return (u"both",[u"sto", u"sta", u"što", u"šta"])
    elif (u"sto" in tok) or (u"što" in tok):
        return (u'sto', [u"sto", u"što"])
    elif (u"sta" in tok) or (u"šta" in tok):
        return (u'sta',[u"sta", u"šta"])
    else:
        return u'NA'

def da_je_li(text):
    """returns "da li" if "da li" in tweet and "je li" if "je li" in tweet
     "both" if both and "NA" if none"""
    text = text.lower()
    dali_re=re.findall(ur'\b(da li|dal)\b',text, re.UNICODE)
    jeli_re=re.findall(ur'\b(je li|jel)\b',text, re.UNICODE)
    if dali_re and jeli_re:
        return (u"both",dali_re+jeli_re)
    elif dali_re:
        return (u'dali',dali_re)
    elif jeli_re:
        return (u'jeli', jeli_re)
    else:
        return u'NA'
#
def usprkos(text):
    text_withoutdia = text.lower()
    if u'usprkos' in text_withoutdia:
        return (u'usprkos', [u'usprkos'])
    elif u'uprkos' in text_withoutdia:
        return (u'uprkos', [u'uprkos'])
    elif u'unatoc' in text_withoutdia:
        return (u'unatoc', [u'unatoc', u'unatoč'])
    else:
        return u"NA"

def treba_da(text):
    """returns "treba da" if "treba da" in tweet and "trebaX da" if treba\w+\sda in tweet (ex. trebam da)
     "both" if both and "NA" if none"""
    """" treba da vs. treba* da """""
    text = text.lower()
    trebada_all=re.findall(ur'(\b(treba|trebalo je|trebalo bi)\sda\b)',text, re.UNICODE)
    trebaXsg_all=re.findall(ur'(\btreba(m|s|mo|te|ju)\sda\b)',text,re.UNICODE)
    trebaXpl_all=re.findall(ur'(\btreba(la|o|li|le)\s(sam|si|je|smo|ste|su|bi)\sda\b)',text,re.UNICODE)

    trebada = [mymatch[0] for mymatch in trebada_all]
    trebaXsg = [mymatch[0] for mymatch in trebaXsg_all]
    trebaXpl = [mymatch[0] for mymatch in trebaXpl_all]

    if trebada and (trebaXsg or trebaXpl):
        return (u"both", trebada+trebaXsg+trebaXpl)
    elif trebada:
        return (u"treba-da",trebada)
    elif trebaXsg:
        return (u"trebax-da",trebaXsg)
    elif trebaXpl:
        return  (u"trebax-da",trebaXpl)
    else:
        return u"NA"


 #or find all the declination of treba in the lexicon - much more precise

# def treba(text):
#
#     text = text.lower()
#     treba_all=re.findall(ur'(\btreba|trebalo je|trebalo bi\b)',text, re.UNICODE)
#     trebaXsg_all=re.findall(ur'(\btreba(m|s|mo|te|ju)\b)',text,re.UNICODE)
#     trebaXpl_all=re.findall(ur'(\btreba(la|o|li|le)\s(sam|si|je|smo|ste|su|bi)\b)',text,re.UNICODE)
#
#     trebada = [mymatch[0] for mymatch in treba_all]
#     trebaXsg = [mymatch[0] for mymatch in trebaXsg_all]
#     trebaXpl = [mymatch[0] for mymatch in trebaXpl_all]
#
#     if trebada and (trebaXsg or trebaXpl):
#         return (u"both", trebada+trebaXsg+trebaXpl)
#     elif trebada:
#         return (u"treba",trebada)
#     elif trebaXsg:
#         return (u"trebax",trebaXsg)
#     elif trebaXpl:
#         return  (u"trebax",trebaXpl)
#     else:
#         return u"NA"
#
#
#
def bre(text):
   # """ returns  bre, bolan, ba or NA, depending on the presence of thise stings in tweets """
    tok = tokenize(text.lower())
    if u"bre" in tok:
        return (u'bre', [u'bre'])
    elif u"bolan" in tok or u"bona" in tok:
        return (u'bolan',[u'bolan',u'bona'])
    elif u"ba" in tok:
        return (u'ba',[u'ba'])
    else:
        return u'NA'
#
def mnogo(text):
    #TODO check if it makes sense
    tok = tokenize(text.lower())

    #for token in tokenize(text):
    if u"mnogo" in tok:
        return (u'mnogo',[u'mnogo'])
    elif u"puno" in tok:
        return (u'puno',[u'puno'])
    elif u"vrlo" in tok:
        return (u'vrlo',[u'vrlo'])
    elif u"jako" in tok:
        return (u'jako',[u'jako'])
    else:
        return u"NA"
#
def months(text):
    """returns "HR months" if croatian month names and "international months"
     if international, both if both and NA if none  """

    # TODO if not Maja (m uppercase) or maja \w+i(c|ć)

    text = text.lower()
    hr,international = [],[]
    for token in tokenize(text):
        if token in hrmonths:
            hr.append(token)
        elif token in intmonths:
            international.append(token)
    if len(hr)>0 and len(international)>0:
        return (u"both",hr+international)
    elif len(hr)>0:
        return (u"hr-months",hr)
    elif len(international)>0:
        return (u"int-months",international)
    else:
        return u"NA"
#
def tjedan(text):
    """returns tjedan/sedmica/nedjelja/nedelja/NA """
    text = text.lower()
    tjedan_re_all=re.findall(ur'\btjed(an|na|no|nu|nom|ni|ana|nima)\b',text ,re.UNICODE)
    sedmica_re_all=re.findall(ur'\bsedmic(a|u|i|om|e|ama)\b',text, re.UNICODE)
    nedjelja_re_all=re.findall(ur'\bnedjelj(a|u|i|om|e|ama)\b',text,re.UNICODE)
    nedelja_re_all=re.findall(ur'\bnedelj(a|u|i|om|e|ama)\b',text,re.UNICODE)

    tjedan_re = [mymatch[0] for mymatch in tjedan_re_all]
    sedmica_re = [mymatch[0] for mymatch in sedmica_re_all]
    nedjelja_re = [mymatch[0] for mymatch in nedjelja_re_all]
    nedelja_re = [mymatch[0] for mymatch in nedelja_re_all]

    if tjedan_re:
        return (u"tjedan",tjedan_re)
    elif sedmica_re:
        return (u"sedmica",sedmica_re)
    elif nedjelja_re:
        return (u"nedjelja",nedjelja_re)
    elif nedelja_re:
        return (u"nedelja",nedelja_re)
    else:
        return u"NA"
#
def drug(text):
    """returns drug/prijatelj/both/NA"""
    # TODO 1: include variations such as drugaricin, drugarski etc?
    # TODO 2: get rid of flase positivs like na drugom, nekom drugom, jedno drugo, drugu stranu, drugu sezonu, druga osoba

    text = text.lower()
    drug_all=re.findall(ur'\b(drug(a|u|om|ovi|ove|ovima)?|druze|drugaric(a|e|i|om|ama))\b',text,re.UNICODE)
    prijatelj_all=re.findall(ur'\b(prijatelj(a|u|em|e|ima)?|prijateljic(a|u|e|i|om|ama))\b', text,re.UNICODE)


    drug = [mymatch[0] for mymatch in drug_all]
    prijatelj = [mymatch[0] for mymatch in prijatelj_all]

    if drug and prijatelj:
        return (u"both",drug+prijatelj)
    elif drug:
        return (u"drug",drug)
    elif prijatelj:
        return (u"prijatelj",prijatelj)
    else:
        return u"NA"
#
#
# #---End Lexical Features -----------------------------------------------------------------------------------------------
#
# #---Start Morpho-Synt. Features ----------------------------------------------------------------------------------------
#
# # – infinitive without ”i”
#
def inf_without_i(text):

  """return "inf without i" if infinitiv without -i ending and "inf with i" if infinitiv with -i ending,
   both if both and NA if none"""

  # TODO if prev. token not prep like pred, na, po, etc.

  text = text.lower()
  distr_no_i,distr_i=[],[]
  for token in tokenize(text):
      if token.endswith(u"c") or token.endswith(u"ć") or token.endswith(u"t"):
          mod_token = token+u"i"
          if mod_token in inf_dict:
              distr_no_i.append(mod_token)
      elif token.endswith(u"ci") or token.endswith(u"ći") or token.endswith(u"ti"):
          if token in inf_dict:
              distr_i.append(token)
  if len(distr_no_i)>0 and len(distr_i)>0:
      return (u"both", distr_no_i+distr_i)
  elif len(distr_no_i)>0:
    return (u"inf-i-drop", distr_no_i)
  elif len(distr_i)>0:
    return (u"inf-i",distr_i)
  else:
    return u"NA"
#
# #– synthetic future tense
# #syntinfverbs
#

def synt_future(text):
  """return "synt inf" if syntetic infinitiv (uradicu), "nosynt inf" if analytic infinitiv (uradit cu),
  "both" if both and NA if none """
  distrsynt, distrnosynt = [],[]
  tokenized = tokenize(text.lower())
  biti = [u"cu", u"ces", u"ce", u"cemo", u"cete"]
  for token in tokenized[:-1]:
    if token in synt_futur_dict:
        distrsynt.append(token)
        # take both variations (doc cu/doc cu) as correct (because they serve the purpose)
    if (token in inf_dict or token[:-1] in inf_dict) \
            and remove_diacritics(tokenized[tokenized.index(token)+1]) in biti:
        distrnosynt.append(token)
  if len(distrsynt)>0 and len(distrnosynt)>0:
      return (u"both",distrsynt+distrnosynt)
  elif len(distrsynt)>0:
      return (u"synt-future",distrsynt)
  elif len(distrnosynt)>0:
      return (u"anal-future",distrnosynt)
  else:
      return u"NA"
#
def da(text):
    """return "da" if da in text and NA if not"""
    if u"da" in tokenize(text.lower()):
        return (u"da",[])
    else:
        return u"NA"
#
#
#
def da_present(text):
    """"return "da pres" if "da" is followed by verb in present tense in the +2 window,
      "da without pres" if it is not, and NA if there is no "da" in the tweet  """
    ## TODO solve problem ---bla bla da ces----
    text = text.lower()
    if u"da" in tokenize(text)[1:-2]:
        dasent = tokenize(text)
        ## if we want to add a condition before "da"
        if dasent[dasent.index(u"da")-1] in modalverbs:
            if dasent[dasent.index(u"da")+2] in presverbs:
            #print dasent[dasent.index("da")+2], type(dasent[dasent.index("da")+2])
                return (u"da-pres", [u"da"])#+u" "+dasent[dasent.index(u"da")+2]])
            else:
                return u"NA"
        else:
            return u"NA"
    if u"da" in tokenize(text)[1:-1]:
        dasent = tokenize(text)
        ## if we want to add a condition before "da"
        if dasent[dasent.index(u"da")-1] in modalverbs:
            if dasent[dasent.index(u"da")+1] in presverbs:
                return (u"da-pres", [u"da"])#+u" "+dasent[dasent.index(u"da")+1]])
            else:
                return u"NA"
        else:
            return u"NA"
    else:
        return u"NA"

#
def genitiva(text):
    """return "oga" if a word in tweet is ending with -oga and is in the list of genitiv-(o|e)g/a endings
      "og/eg" if a word in tweet is ending with -og/eg and is in the list of genitiv-og/a endings,
       both if both and NA if none"""
    # TODO decide whether to do the same for -ome, -om
    distr_og,distr_oga=[],[]
    tokenized = tokenize(text.lower())
    for token in tokenized:
        if token in genitiv_og_dict:
            distr_og.append(token)
        else:
            if token.endswith(u"ga") and (token[:-1] in genitiv_og_dict):
                distr_oga.append(token)
    if len(distr_og)>0 and len(distr_oga)>0:
        return (u"both",distr_og+distr_oga)
    elif len(distr_og)>0:
        return (u"og",distr_og)
    elif len(distr_oga)>0:
        return (u"oga",distr_oga)
    else:
        return u"NA"


def ir_is(text):
    myir_is=check_var_in_tab_sep_lexicons(text,ir_is_dict)
    return myir_is
#
def ir_ov(text):
    myir_ov=check_var_in_tab_sep_lexicons(text,ir_ov_dict)
    return myir_ov

#
def inf_verb_ratio(text):
    """return ratio nr.infinitiv/nr.allverbs """
    # TODO: if uradicu infinitiv
    nr_verbs = 0
    nr_inf = 0
    for token in tokenize(text.lower()):
        if token in verbs_dict:
            nr_verbs+=1
            if (token in inf_dict) or (token in synt_futur_dict):
                nr_inf+=1
    if nr_verbs>0:
        return (str(round(nr_inf/nr_verbs,2)),[])
    else:
        return u"NA"

# #---End Morpho-Synt. Features ------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
## To be considered in the next version!

# def budem(text):
#     budemlist=[u"budem", u"budeš", u"budes", u"bude", u"budemo",u"budete", u"budu"]
#     budemdistr=[]
#     for token in tokenize(text.lower()):
#         if token in budemlist:
#             budemdistr.append(budemlist[budemlist.index(token)])
#     if len(budemdistr)>0:
#         return (u"budem", budemdistr)
#     else:
#         return u"NA"
#
#
# def desiti(text):
#     distr_dog, distr_des=[],[]
#     for token in tokenize(text.lower()):
#         if token in dog:
#             distr_dog.append(token)
#         elif token in des:
#             distr_des.append(des)
#     if len(distr_dog)>0 and len(distr_des)>0:
#         return (u"both", distr_dog+distr_des)
#     elif len(distr_dog)>0:
#         return (u"dogoditi", distr_dog)
#     elif len(distr_des)>0:
#         return (u"desiti", distr_des)
#     else:
#         return "NA"


#-------------------------------------------------------------------------------------
#

def cyrillic(text):
    """Check if cyrillic letters in text"""
   # text=text.decode("utf8")
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
       return (u"sr-cyr",[])
    elif len(not_sr_cyril)>len(sr_cyril):
       return (u"mix-cyr",[])
    else:
       return (u"latin",[])


def highlight_var(myfunctionvalue,text):
    for word in myfunctionvalue:
        text = re.sub(ur'\b'+re.escape(word)+ur'\b', u'__'+word+u'__', text, re.UNICODE)
    return text



def replacetext(myfunc,mytext):
    if not myfunc==u"NA":
        mytext=highlight_var(myfunc[1], mytext)
    else:
        mytext=mytext
    return  mytext



t="\t"
out=gzip.open('hrsrTweets.var.gz','w')
out.write('tid'+t+'user'+t+'time'+t+'lang'+t+'lon'+t+'lat'+t+'text'+t+"text_meta"+t+"yat"+t+"kh"+t+"hdrop"+t+"rdrop"+t
              +"st_c"+t+"c_ch"+t+"diftong"+t
              +"sa_s"+t+"tko_ko"+t+"sta_sto"+t+"da_je_li"+t
              +"usprkos"+t+"bre"+t+"mnogo"+t
              +"months"+t+"tjedan"+t
              +"drug"+t+"treba_da"+t
              +"inf_without_i"+t+"synt_future"+t+"da"+t
              +"da_present"+t+"genitiva"+t+"ir_is"+t
              +"ir_ov"+t+"inf_verb_ratio"+t
              +"cyrillic"+"\n")


for line in gzip.open('hrsrTweets.gz'):
    tid,user,time,lang,lon,lat,text=line[:-1].decode('utf8').split('\t')

    clean_var=clean(text,lang)

    l=[yat(text),kh(text),hdrop(text),rdrop(text),st_c(text),c_ch(text),diftong(text),sa_s(text),tko_ko(text),sta_sto(text),
    da_je_li(text),usprkos(text),bre(text),mnogo(text),months(text),tjedan(text),drug(text),treba_da(text),inf_without_i(text),
    synt_future(text),da(text),da_present(text),genitiva(text),ir_is(text),ir_ov(text),inf_verb_ratio(text),cyrillic(text)]

    for myfuncvar in l:
        text=replacetext(myfuncvar,text)

    myvariables = u"\t".join([returned[0] if type(returned)==tuple else u"NA" for returned in l])

    out.write(tid.encode("utf8")+"\t"+user.encode("utf8")+"\t"+time.encode("utf8")+"\t"+lang.encode("utf8")+"\t"
             +lon.encode("utf8")+"\t"+lat.encode("utf8")+"\t"
             +text.encode("utf8")+"\t"+clean_var.encode("utf8")+"\t"
             +myvariables.encode("utf8")+"\n")
out.close()
