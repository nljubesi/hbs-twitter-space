#!/usr/bin/python
#-*-coding:utf8-*-
import gzip
import sys
from collections import defaultdict

lexicon_dirs='../../lexicons/apertium'
stem_dict = defaultdict(int)

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(token):
  result=''
  for char in token:
    result+=dia.get(char,char)
  return result

log=open('log','w')
inter_stem_lex=open('inter_stem_lex.txt', 'w')
hr=defaultdict(list)
sr=defaultdict(list)
for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  hr[lemma]+=[token]


for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_SR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  sr[lemma]+=[token]


for lemma in hr:
    if lemma.endswith("irati") and len(lemma)>7:
        mod_lemma_ovati = lemma[:-5]+"ovati"
        mod_lemma_isati = lemma[:-5]+"isati"

        if mod_lemma_ovati in sr: # mod_lemma_isati in sr:
           stem_dict[lemma[:-5]]+=1
           stem_dict[mod_lemma_ovati[:-5]]+=1
           log.write(repr('candidate '+lemma+' '+mod_lemma_ovati)+'\n')
           dia_lemma=remove_diacritics(lemma)
           if dia_lemma!=lemma:
               dia_mod_lemma_ovati=remove_diacritics(mod_lemma_ovati)
               if dia_lemma not in hr and dia_mod_lemma_ovati not in hr:# and dia_mod_lemma_isati not in hr:
                   log.write('dia not in lexicons\n')
                   stem_dict[dia_mod_lemma_ovati[:-5]]+=1

        if mod_lemma_isati in sr: # mod_lemma_isati in sr:
           stem_dict[mod_lemma_isati[:-5]]+=1
           log.write(repr('candidate '+lemma+' '+mod_lemma_isati)+'\n')
           dia_lemma=remove_diacritics(lemma)
           if dia_lemma!=lemma:
               dia_mod_lemma_isati=remove_diacritics(mod_lemma_isati)
               if dia_lemma not in hr and dia_mod_lemma_isati not in hr:# and dia_mod_lemma_isati not in hr:
                   log.write('dia not in lexicons\n')
                   stem_dict[mod_lemma_isati[:-5]]+=1

for stem in stem_dict:
    inter_stem_lex.write(stem.encode('utf8')+'\n')


