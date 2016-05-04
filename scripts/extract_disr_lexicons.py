#!/usr/bin/python
#-*-coding:utf8-*-
import gzip


lexicon_dirs='../../lexicons/apertium'
yat=gzip.open('../custom-lexicons/yat-lexicon.gz','w')
diftong_v=gzip.open('../custom-lexicons/diftong-v-lexicon.gz','w')
h_drop=gzip.open('../custom-lexicons/hdrop-lexicon.gz','w')
k_h=gzip.open('../custom-lexicons/kh-lexicon.gz','w')
st_c=gzip.open('../custom-lexicons/st-c-lexicon.gz','w')
ir_is=gzip.open('../custom-lexicons/ir-is-lexicon.gz', 'w')
ir_ov=gzip.open('../custom-lexicons/ir-ov-lexicon.gz', 'w')


## Open dicts for preventing duplicates
yat_dict, diftong_v_dict, h_drop_dict, k_h_dict, st_c_dict, ir_is_dict, ir_ov_dict = {},{},{},{},{},{},{}

## Eventually for ist/ista feature (ex. vizazist/vizazista)
# ist=gzip.open('custom-lexicons/apertium-ist-lexicon.gz','w')

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(token):
  result=''
  for char in token:
    result+=dia.get(char,char)
  return result

log=open('log','w')
hr={}
sr={}
hr_lemma={}
sr_lemma={}


for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_HR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  if token not in hr:
    hr[token]=set()
  hr[token].add(tag)
  if lemma not in hr_lemma:
    hr_lemma[lemma]=set()
  hr_lemma[lemma].add(token)
log.write(repr(hr.items()[:10])+'\n')


for line in gzip.open(lexicon_dirs+'/apertium-hbs.hbs_SR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  if token not in sr:
    sr[token]=set()
  sr[token].add(tag)
  if lemma not in sr_lemma:
    sr_lemma[lemma]=set()
  sr_lemma[lemma].add(token)
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
                    yat_dict[token]="je"
                    yat_dict[mod_token]="e"
                    yat_dict[dia_token]="je"
                    yat_dict[dia_mod_token]="e"

    if token.startswith("k"):
        mod_token = token[0].replace('k','h')+token[1:]
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               if mod_token not in hr:
                   dia_token=remove_diacritics(token)
                   dia_mod_token=remove_diacritics(mod_token)
                   k_h_dict[token]="k"
                   k_h_dict[mod_token]="h"
                   k_h_dict[dia_token]="k"
                   k_h_dict[dia_mod_token]="h"

    if token.startswith("h"):
        mod_token = token[1:]
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               if mod_token not in hr:
                   log.write('not in hr\n')
                   dia_token=remove_diacritics(token)
                   dia_mod_token=remove_diacritics(mod_token)
                   h_drop_dict[token]="h"
                   h_drop_dict[mod_token]="h_drop"
                   h_drop_dict[dia_token]="h"
                   h_drop_dict[dia_mod_token]="h_drop"

    if "eu" or "au" in token:
        mod_token = token.replace('eu','ev').replace("au", "av")
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               if mod_token not in hr:
                   log.write('not in hr\n')
                   dia_token=remove_diacritics(token)
                   dia_mod_token=remove_diacritics(mod_token)
                   diftong_v_dict[token]="eu/au"
                   diftong_v_dict[mod_token]="ev/av"
                   diftong_v_dict[dia_token]="eu/au"
                   diftong_v_dict[dia_mod_token]="ev/av"

    if u"ć" in token:
        mod_token = token.replace(u'ć',u'št')
        if mod_token in sr:
           log.write(repr('candidate '+token+' '+mod_token)+'\n')
           if len(hr[token].intersection(sr[mod_token]))>0:
               if mod_token not in hr:
                   log.write('not in hr\n')
                   dia_token=remove_diacritics(token)
                   dia_mod_token=remove_diacritics(mod_token)
                   st_c_dict[token]="ć"
                   st_c_dict[mod_token]="št"
                   st_c_dict[dia_token]="ć"
                   st_c_dict[dia_mod_token]="št"


for lemma in hr_lemma:
    # get the stem if croatian lemma ends with -irati and if it's longer than 7 characters
    #  (arbitrary value to avoid false positivs)
    # TODO examples of false positivs we are avoiding
    if lemma.endswith("irati") and len(lemma)>7:
        mod_lemma_ovati = lemma[:-5]+"ovati"
        mod_lemma_isati = lemma[:-5]+"isati"

        # if the same stem is present in serbian Apertium with the ending -ovati,
        # write the stem in the output list (without diactritics)
        if mod_lemma_ovati in sr_lemma: # mod_lemma_isati in sr:
           if mod_lemma_ovati not in hr_lemma:
               for mytoken in sr_lemma[mod_lemma_ovati]:
                   dia_token = remove_diacritics(mytoken)
                   ir_ov_dict[mytoken]="ovati"
                   ir_ov_dict[dia_token]="ovati"
               for mytoken in hr_lemma[lemma]:
                   dia_token = remove_diacritics(mytoken)
                   ir_ov_dict[mytoken]="irati"
                   ir_ov_dict[dia_token]="irati"

        if mod_lemma_isati in sr_lemma: # mod_lemma_isati in sr:
           if mod_lemma_isati not in hr_lemma:
               for mytoken in sr_lemma[mod_lemma_isati]:
                   dia_token = remove_diacritics(mytoken)
                   ir_is_dict[mytoken]="isati"
                   ir_is_dict[dia_token]="isati"
               for mytoken in hr_lemma[lemma]:
                   dia_token = remove_diacritics(mytoken)
                   ir_is_dict[mytoken]="irati"
                   ir_is_dict[dia_token]="irati"


def writeinfile(mydict,myout):
    for token in sorted(mydict):
        myout.write(token.encode("utf8")+"\t"+mydict[token]+"\n")
    myout.close()
    return myout


writeinfile(yat_dict,yat)
writeinfile(diftong_v_dict,diftong_v)
writeinfile(h_drop_dict,h_drop)
writeinfile(k_h_dict,k_h)
writeinfile(st_c_dict,st_c)
writeinfile(ir_is_dict,ir_is)
writeinfile(ir_ov_dict,ir_ov)


    ## eventually  for creating -ist lexicon (vizazist)
    ## problem: false positivs

    #if tag == u"Ncmsn" and token.endswith(u"ist"):
        #dia_token=remove_diacritics(token)
        #if dia_token!=token:
        #    ist.write(dia_token.encode('utf8')+'\n')
