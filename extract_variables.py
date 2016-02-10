#!/usr/bin/python
#-*-coding:utf8-*-

## TODO if sentence contains both features
## – infinitive / verb ratio
## – ”da”
#£ – te / pa, pa relative frequency (difficult because of te personal pronoun)


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

lexicon_dirs='../lexicons/apertium'
token_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+|\w+',re.UNICODE)
yat_lexicon=dict([e[:-1].split('\t') for e in gzip.open('yat-lexicon/apertium-yat.gz')])
kh_lexicon=dict([k[:-1].split('\t') for k in gzip.open('kh-lexicon/apertium-kh.gz')])
hdrop_lexicon=dict([h[:-1].split('\t') for h in gzip.open('drop-lexicon/apertium-hdrop.gz')])

#modals=codecs.open('modals/modals.txt', 'r', 'utf8')
#for modalverb in modals:
 #   modalverb = modalverb.rstrip("\n")
 #   modalsdict[modalverb]+=1

rdrop_lexicon={}
for x in gzip.open('drop-lexicon/apertium-rdrop.gz'):
    rdrop_lexicon[remove_diacritics(x[:-1].split()[0].decode('utf8'))]=x[:-1].split()[1]

stems_dict=defaultdict(int)
stems=codecs.open('ir-ov-is/inter_stem_lex.txt', 'r', 'utf8')
for stem in stems:
    stems_dict[stem[:-1]]+=1

genitivoga_re=re.compile(r'og\t\w+\t\w+(m|n)sg(y)?$',re.UNICODE)
ch_dict,infverbs,syntinfverbs,modalsdict,genitiv_og = defaultdict(int),defaultdict(int),defaultdict(int),defaultdict(int),defaultdict(int)
presverbs=defaultdict(unicode)


for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if u"ć" or u"č" in token:
      ch_dict[token]+=1
  ## if infinitiv with -i
  if tag == u'Vmn':
      tokennodia = remove_diacritics(token)
      infverbs[tokennodia]+=1
  ## if presäns:
  elif tag.startswith(u"Vmr"):
      tokennodia = remove_diacritics(token)
      presverbs[tokennodia]+=tag
  ## if genitiv ending with og
  elif token.endswith(u"og") and u"msgy" in tag or u"nsgy" in tag:
      # pidjevi +  zamjenice (onog, tog, itd)
      # ako samo pridjevi: add y poslije (m|n)sg (slijepoga	slijep	Agpmsgy)
      # problem "Iz nekog švajcarskog sela bi bilo korektnije vs lako je naci nekog sa kim cete ziveti tesko je pronaci nekog u kome cete ziveti"
      tokennodia = remove_diacritics(token)
      genitiv_og[tokennodia]+=1

for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_SR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if u"ć" or u"č" in token:
      ch_dict[token]+=1
  ## if infinitiv with -i
  if tag == u'Vmn':
      tokennodia = remove_diacritics(token)
      infverbs[tokennodia]+=1
  ## if synt.infinitiv
  elif tag.startswith(u'Vmf'):
      tokennodia = remove_diacritics(token)
      syntinfverbs[tokennodia]+=1
  ## if presäns:
  elif tag.startswith(u"Vmr"):
      tokennodia = remove_diacritics(token)
      presverbs[tokennodia]+=tag
  ## if genitiv ending with og
  elif token.endswith(u"og") and u"msg" in tag or u"nsg" in tag:
      tokennodia = remove_diacritics(token)
      genitiv_og[tokennodia]+=1


#TODO: rdrop lexicon is to be extended (apertium is not a good resource for this)
#TODO: ldrop lexicon is to be made (apertium is not a good resource for this)


def tokenize(text):
  return token_re.findall(text)


##---Start Cleanining Features------------------------------------------------------------------------------------------


def clean(text,lang):
    automatic_re = re.search("(Objavio/la sam novu fotografiju|Just posted a photo|Today stats:|I just ousted|I'm at|I (just)? ?(voted|added)|via (Tumblr|Facebook)|I liked a @YouTube)",text)
    if automatic_re or "tweep" in "automatically checked by" in text:
        return "automatic"
    elif lang.startswith("en:1"):
         return "english_tweet"
    elif lang.startswith("en:") and "if you" in text or " visit " in text:
         return "english_tweet"

    else:
        if len(tokenize(text))==2:
             emoji_punct_website_re = re.search("^[^A-Za-z]+ ?http.+$",text,re.UNICODE)
             user_website_re = re.search("^@.+ ?http.+$",text,re.UNICODE)
             user_puncta = re.search("^@.+ ?[^A-Za-z]+$",text,re.UNICODE)
             user_punctb = re.search("[^A-Za-z]+ ?@.+?$",text,re.UNICODE)
             if emoji_punct_website_re or user_website_re:
                 return "noise_website"
             elif user_puncta or user_punctb:
                 return "noise_user"
             else:
                 return "NA"
        elif len(tokenize(text)) == 1:
            only_punct_re = re.search("^[^A-Za-z]+$",text,re.UNICODE)
            if "".join(tokenize(text)).startswith("http"):
                return "website"
            elif only_punct_re:
                return "is_not_alpha"
            else:
                return "NA"
        else:
            return "NA"
            #eventually:
            #other_non_bkms_tweets_re = re.search("\w+? ?(Follow me on|check (this)? ?out|you should|untitled)",text)
            #if other_non_bkms_tweets_re:
             #   return "other"


##--- End Cleanining Features-------------------------------------------------------------------------------------------

#---Start Phonetical Features-------------------------------------------------------------------------------------------

def yat(text):
  # TODO IF BOTH CONDITIONS ARE TRUE
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
    # TODO IF BOTH CONDITIONS ARE TRUE
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
  if len(distr_ch)==1:
    return "č_dev"
  elif len(distr_c)==1:
    return "ć_dev"
  else:
    return "NA"


#---End Phonetical Features---------------------------------------------------------------------------------------------

#---Start Lexical Features----------------------------------------------------------------------------------------------


def sa_s(text):
    # TODO IF BOTH CONDITIONS ARE TRUE

    """" sa / s rule deviation
    #http://savjetnik.ihjj.hr/savjet.php?id=17
    #Prijedlog sa upotrebljava se samo ispred riječi koje počinju glasovima s, š, z, ž
    #other (more complicated) source http://jezicna-pomoc.lss.hr/jsavjeti.php?view=2"""""

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
    #(...) sve sto ides dalje to je teze i teze, ali sta je tu je :D
    #Note: što interrogative meaning same for all languages:  Sto da ne
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
    else:
        return "NA"

#Možeš nešto da ne razumeš, ali ne bi trebalo da samo zbog toga to i ne poštuješ.

def treba_da(text):
    """" treba da vs. treba* da """""
    text_withoutdia = remove_diacritics(text).lower()
    trebada=re.search(r'\b(treba|trebalo je|trebalo bi)\sda\b',text_withoutdia, re.UNICODE)
    trebaXsg=re.search(r'\btreba(m|s|mo|te|ju)\sda\b',text_withoutdia, re.UNICODE)
    trebaXpl=re.search(r'\btreba(la|o|li|le)\s(sam|si|je|smo|ste|su|bi)\sda\b',text_withoutdia, re.UNICODE)

    if trebada:
        return "treba_da"
    elif trebaXsg or trebaXpl:
        return "trebaX_da"
    else:
        return "NA"

#---End Lexical Features -----------------------------------------------------------------------------------------------

#---Start Morpho-Synt. Features ----------------------------------------------------------------------------------------

# – infinitive without ”i”

def inf_without_i(text):
  text_withoutdia = remove_diacritics(text).lower()
  distr_no_i,distr_i=defaultdict(int), defaultdict(int)
  for token in tokenize(text_withoutdia):
      if token.endswith(u"c") or token.endswith(u"t"):
          mod_token = token+u"i"
          if mod_token in infverbs:
              distr_no_i[mod_token]+=1
      elif token.endswith(u"ci") or token.endswith(u"ti"):
          if token in infverbs:
              distr_i[token]+=1
  if len(distr_no_i)>=1:
    return "inf_without_i"
  elif len(distr_i)>=1:
    return "inf_with_i"
  else:
    return "NA"

#– synthetic future tense
#syntinfverbs

def synt_future(text):
    #http://stackoverflow.com/questions/8923729/checking-for-diacritics-with-a-regular-expression
  distrsynt, distrnosynt = defaultdict(int), defaultdict(int)
  text_withoutdia = remove_diacritics(text).lower()
  syntend_re=re.search(ur'\s(\w+(cu|ces|ce|cemo|cete|ce))\s',text_withoutdia, re.UNICODE)
  nosyntend_re=re.search(ur'\s(\w+(t|c)) (cu|ces|ce|cemo|cete|ce)\s',text_withoutdia, re.UNICODE)

  if syntend_re:
      if syntend_re.group(1) in syntinfverbs:
          distrsynt[syntend_re.group(1)]+=1
  elif nosyntend_re:
      if nosyntend_re.group(1) in infverbs or nosyntend_re.group(1)+u"i" in infverbs:
          distrnosynt[nosyntend_re.group(1)]+=1
  if len(distrsynt)>=1:
    return "synt_inf"
  elif len(distrnosynt)>=1:
    return "nosynt_inf"
  else:
    return "NA"

# – da + present tense ####### djelom vec u treba da
# sad će da ti uputi otvoreno pismo pa ćeš da vidiš

def da_present(text):

    text_withoutdia = remove_diacritics(text).lower()
    if "da" in tokenize(text_withoutdia)[1:-2]:
        dasent = tokenize(text_withoutdia)
        ##if we want to add a condition before "da"
        #if #dasent[dasent.index("da")-1] in presverbs/modalverbs and
        if dasent[dasent.index("da")+2] in presverbs:
            return "da_pres"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        elif dasent[dasent.index("da")+2] not in presverbs:
            return "da_no_pres"
        else:
            return "NA"
    elif "da" in tokenize(text_withoutdia)[1:-1]:
        dasent = tokenize(text_withoutdia)
        ##if we want to add a condition before "da"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        if  dasent[dasent.index("da")+1] in presverbs:
            return "da_pres"
        #dasent[dasent.index("da")-1] in presverbs/modalverbs  and
        elif  dasent[dasent.index("da")+1] not in presverbs:
            return "da_no_pres"
        else:
            return "NA"
    else:
        return "NA"


def genitiva(text):
    # TODO nekog/onog/tog etc.
    # TODO #ome, om ?
    text_withoutdia = remove_diacritics(text).lower()
    oga_re=re.search(ur'\b(\w+oga)\b',text_withoutdia, re.UNICODE)
    og_re=re.search(ur'\b(\w+og)\b',text_withoutdia, re.UNICODE)
    if oga_re:
        #print oga_re.group(1)
        if oga_re.group(1)[:-1] in genitiv_og:
            return "oga"
        else:
            return "NA"
    elif og_re:
        if og_re.group(1) in genitiv_og:
            return "og"
        else:
            return "NA"
    else:
        return "NA"

def ir_ov_is(text):
    # TODO nekog/onog/tog etc.
    # TODO #ome, om ?

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



#---End Morpho-Synt. Features ------------------------------------------------------------------------------------------



out=gzip.open('hrsrTweets.var.gz','w')
for line in gzip.open('hrsrTweets.gz'):
    tid,user,time,lang,lon,lat,text=line[:-1].decode('utf8').split('\t')
    #print hdrop(text)#, #text.encode("utf8")
    out.write(line[:-1]+"\t"+clean(text,lang)+'\t'+yat(text)+'\t'+kh(text)+"\t"+hdrop(text)+"\t"+rdrop(text)+"\t"+c_ch(text)+"\t"+sa_s(text)+"\t"+tko_ko(text)+"\t"+sta_sto(text)+"\t"+da_je_li(text)+"\t"+usprkos(text)+"\t"+treba_da(text)+"\t"+inf_without_i(text)+"\t"+synt_future(text)+"\t"+da_present(text)+"\t"+genitiva(text)+"\t"+ir_ov_is(text)+'\n')



out.close()
