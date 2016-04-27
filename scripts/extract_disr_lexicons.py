#!/usr/bin/python
#-*-coding:utf8-*-
import gzip


lexicon_dirs='../../lexicons/apertium'
yat=gzip.open('../custom-lexicons/apertium-yat-lexicon.gz','w')
diftong_v=gzip.open('../custom-lexicons/apertium-diftong-v-lexicon.gz','w')
h_drop=gzip.open('../custom-lexicons/apertium-hdrop-lexicon.gz','w')
k_h=gzip.open('../custom-lexicons/apertium-kh-lexicon.gz','w')
st_c=gzip.open('../custom-lexicons/apertium-st-c-lexicon.gz','w')
##eventually for ist/ista feature (ex. vizazist/vizazista)
#ist=gzip.open('custom-lexicons/apertium-ist-lexicon.gz','w')

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(token):
  result=''
  for char in token:
    result+=dia.get(char,char)
  return result

log=open('log','w')
hr={}
sr={}
for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  if token not in hr:
    hr[token]=set()
  hr[token].add(tag)
log.write(repr(hr.items()[:10])+'\n')


for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_SR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  if token not in sr:
    sr[token]=set()
  sr[token].add(tag)
log.write(repr(sr.items()[:10])+'\n')



for index,token in enumerate(hr):
    if index%100==0:
        log.write(str(index+1)+' od '+str(len(hr))+'\n')
    ijee=token.replace('ije','e')
    jee=token.replace('je','e')
    ijej=token.replace('ij','ej')
    for mod_token in (ijee,jee,ijej):
        if token==mod_token:
            continue
        if mod_token in sr:
            log.write(repr('candidate '+token+' '+mod_token)+'\n')
            if len(hr[token].intersection(sr[mod_token]))>0:
                if mod_token not in hr:
                    log.write('not in hr\n')
                    dia_token=remove_diacritics(token)
                    dia_mod_token=remove_diacritics(mod_token)
                    yat.write(dia_token.encode('utf8')+'\tje\n')
                    yat.write(dia_mod_token.encode('utf8')+'\te\n')

    if token.startswith("k"):
        mod_token = token[0].replace('k','h')+token[1:]
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               if mod_token not in hr:
                   dia_token=remove_diacritics(token)
                   dia_mod_token=remove_diacritics(mod_token)
                   k_h.write(dia_token.encode('utf8')+'\tk\n')
                   k_h.write(dia_mod_token.encode('utf8')+'\th\n')
                   log.write('not in hr\n')

    if token.startswith("h"):
        mod_token = token[1:]
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               if mod_token not in hr:
                   log.write('not in hr\n')
                   dia_token=remove_diacritics(token)
                   dia_mod_token=remove_diacritics(mod_token)
                   h_drop.write(token.encode('utf8')+'\th\n')
                   h_drop.write(mod_token.encode('utf8')+'\th_drop\n')

    if "eu" or "au" in token:
        mod_token = token.replace('eu','ev').replace("au", "av")
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               if mod_token not in hr:
                   log.write('not in hr\n')
                   dia_token=remove_diacritics(token)
                   dia_mod_token=remove_diacritics(mod_token)
                   diftong_v.write(dia_token.encode('utf8')+'\teu/au\n')
                   diftong_v.write(dia_mod_token.encode('utf8')+'\tev/av\n')

    if u"ć" in token:
        mod_token = token.replace(u'ć',u'št')
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               if mod_token not in hr:
                   log.write('not in hr\n')
                   dia_token=remove_diacritics(token)
                   dia_mod_token=remove_diacritics(mod_token)
                   st_c.write(dia_token.encode('utf8')+'\tć\n')
                   st_c.write(dia_mod_token.encode('utf8')+'\tšt\n')


    ## eventually  for creating -ist lexicon (vizazist)
    ## problem: false positivs

    #if tag == u"Ncmsn" and token.endswith(u"ist"):
        #dia_token=remove_diacritics(token)
        #if dia_token!=token:
        #    ist.write(dia_token.encode('utf8')+'\n')


yat.close()
diftong_v.close()
h_drop.close()
k_h.close()
st_c.close()
log.close()
#ist.close()