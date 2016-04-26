#!/usr/bin/python
#-*-coding:utf8-*-
import gzip
from collections import defaultdict

# Script for extracting a list of all stems of lemmas from Apertium lexicons
# which end in -irati in Croatian and -ovati or -isati in Serbian

#Call the script with
#$ python extract_irovis_stems.py

lexicon_dirs='../../lexicons/apertium'
stem_dict = defaultdict(int)


dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(token):
  result=''
  for char in token:
    result+=dia.get(char,char)
  return result

log=open('log','w')
inter_stem_lex=gzip.open('../custom-lexicons/inter-stem-lexicon.gz', 'w')
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
    # get the stem if croatian lemma ends with -irati and if it's longer than 7 characters
    #  (arbitrary value to avoid false positivs)
    # TODO examples of false positivs we are avoiding
    if lemma.endswith("irati") and len(lemma)>7:
        mod_lemma_ovati = lemma[:-5]+"ovati"
        mod_lemma_isati = lemma[:-5]+"isati"

        # if the same stem is present in serbian Apertium with the ending -ovati,
        # write the stem in the output list (without diactritics)
        if mod_lemma_ovati in sr: # mod_lemma_isati in sr:
           stem_dict[mod_lemma_ovati[:-5]]+=1
           log.write(repr('candidate '+lemma+' '+mod_lemma_ovati)+'\n')
           dia_lemma=remove_diacritics(lemma)
           if dia_lemma!=lemma:
               dia_mod_lemma_ovati=remove_diacritics(mod_lemma_ovati)
               if dia_lemma not in hr and dia_mod_lemma_ovati not in hr:
                   log.write('dia not in lexicons\n')
                   stem_dict[dia_mod_lemma_ovati[:-5]]+=1

        if mod_lemma_isati in sr:
           stem_dict[mod_lemma_isati[:-5]]+=1
           log.write(repr('candidate '+lemma+' '+mod_lemma_isati)+'\n')
           dia_lemma=remove_diacritics(lemma)
           if dia_lemma!=lemma:
               dia_mod_lemma_isati=remove_diacritics(mod_lemma_isati)
               if dia_lemma not in hr and dia_mod_lemma_isati not in hr:
                   log.write('dia not in lexicons\n')
                   stem_dict[dia_mod_lemma_isati[:-5]]+=1

for stem in stem_dict:
    inter_stem_lex.write(stem.encode('utf8')+'\n')


inter_stem_lex.close()
log.close()