#!/usr/bin/python
#-*-coding:utf8-*-
import gzip
import sys

lexicon_dirs='../../lexicons/apertium'

dia={u'č':'c',u'š':'s',u'ž':'z',u'ć':'c', u'đ':'d'}
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

#večer	večer	Ncfsa
#veče	večer	Ncnsa

for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_SR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  if token not in sr:
    sr[token]=set()
  sr[token].add(tag)
log.write(repr(sr.items()[:10])+'\n')

for token in hr:
    if token.endswith("er"):
        mod_token = token[:-1]
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               #if mod_token not in hr:
               log.write('not in hr\n')
               sys.stdout.write(token.encode('utf8')+'\tr\n')
               sys.stdout.write(mod_token.encode('utf8')+'\tr_drop\n')
               dia_token=remove_diacritics(token)
               if dia_token!=token:
                   dia_mod_token=remove_diacritics(mod_token)
                   if dia_token not in hr and dia_mod_token not in hr:
                       log.write('dia not in lexicons\n')
                       sys.stdout.write(dia_token.encode('utf8')+'\tr\n')
                       sys.stdout.write(dia_mod_token.encode('utf8')+'\tr_drop\n')

    # if token.endswith("l"):
    #     mod_token = token[:-1]
    #     if mod_token in sr:
    #        log.write(repr('candidate '+token+' '+mod_token)+'\n')
    #        if len(hr[token].intersection(sr[mod_token]))>0:
    #            if mod_token not in hr:
    #                log.write('not in hr\n')
    #                sys.stdout.write(token.encode('utf8')+'\tl\n')
    #                sys.stdout.write(mod_token.encode('utf8')+'\tl_drop\n')
    #                dia_token=remove_diacritics(token)
    #                if dia_token!=token:
    #                    dia_mod_token=remove_diacritics(mod_token)
    #                    if dia_token not in hr and dia_mod_token not in hr:
    #                        log.write('dia not in lexicons\n')
    #                        sys.stdout.write(dia_token.encode('utf8')+'\tl\n')
    #                        sys.stdout.write(dia_mod_token.encode('utf8')+'\tl_drop\n')

