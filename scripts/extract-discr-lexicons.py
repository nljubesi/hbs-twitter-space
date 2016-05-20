#!/usr/bin/python
#-*-coding:utf8-*-
import gzip


# TODO:  check the tag of the considered token = tag of the mod token
#vesti - veci

# check the tag of the considered token = tag of the mod token

lexicon_dirs='../../lexicons/apertium'
yat=gzip.open('../custom-lexicons/yat-lexicon.gz','w')
diftong_v=gzip.open('../custom-lexicons/diftong-v-lexicon.gz','w')
h_drop=gzip.open('../custom-lexicons/hdrop-lexicon.gz','w')
k_h=gzip.open('../custom-lexicons/kh-lexicon.gz','w')
st_c=gzip.open('../custom-lexicons/st-c-lexicon.gz','w')
ir_is=gzip.open('../custom-lexicons/ir-is-lexicon.gz', 'w')
ir_ov=gzip.open('../custom-lexicons/ir-ov-lexicon.gz', 'w')

diftong_aueu_in_sr=gzip.open('../evaluation/eval-lexicons/diftong-aueu-in-sr.gz','w')
no_h_drop_in_sr=gzip.open('../evaluation/eval-lexicons/no-h-drop-in-sr.gz','w')
k_in_sr=gzip.open('../evaluation/eval-lexicons/k-in-sr.gz','w')
c_in_sr=gzip.open('../evaluation/eval-lexicons/c-in-sr.gz','w')
irati_in_sr=gzip.open('../evaluation/eval-lexicons/irati-in-sr.gz','w')


## Open dicts for preventing duplicates
yat_dict, diftong_v_dict, h_drop_dict, k_h_dict, st_c_dict, ir_is_dict, ir_ov_dict = {},{},{},{},{},{},{}
diftong_aueu_in_sr_dict, no_h_drop_in_sr_dict, k_in_sr_dict, c_in_sr_dict, irati_in_sr_dict ={},{},{},{},{}

## Eventually for ist/ista feature (ex. vizazist/vizazista)
# ist=gzip.open('custom-lexicons/apertium-ist-lexicon.gz','w')

### up to date TODO idea: ITERATE LEMMAS (not tokens)
# AND IF CONDITION FULLFILLED, TAKE THE TOKEN: LESS WORK TO DO & LESS SUBSTITUTIONS
### to be decided after talking with Nikola and Filip

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(token):
    result=''
    for char in token:
        result+=dia.get(char,char)
    return result


def makedicts(hrout, srout, mydict, diffdict, srlemmadict, hrlemmadict,mod_lemma):
    if mod_lemma in srlemmadict:
        if mod_lemma not in hrlemmadict:
            for mytoken in srlemmadict[mod_lemma]:
                if mytoken not in hr:
                    dia_token = remove_diacritics(mytoken)
                    mydict[mytoken]=srout
                    mydict[dia_token]=srout
            for mytoken in hrlemmadict[lemma]:
                if mytoken not in sr:
                    dia_token = remove_diacritics(mytoken)
                    mydict[mytoken]=hrout
                    mydict[dia_token]=hrout
                else:
                    diffdict[mytoken]=1
    return mydict

log=open('log','w')
hr={}
sr={}
hr_lemma={}
sr_lemma={}


for line in gzip.open(lexicon_dirs+'/hrLex_v1.0.gz'):
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


for line in gzip.open(lexicon_dirs+'/srLex_v1.0.gz'):
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

# The extraction of yat differs from the other extractions because
# 1. yat reflex may be in the lemma but not in the changed word form
# 2. in SR standard there is also IJE/JE whereas other variables are not standard

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



    ## get the stem if croatian lemma ends with -irati and if it's longer than 7 characters
    ##  (arbitrary value to avoid false positivs)
    ## if the same stem is present in serbian Apertium with the ending -ovati,
    ## write the stem in the output list (without diactritics)

for lemma in hr_lemma:
    if lemma.endswith("irati") and len(lemma)>7:

        #TODO exceptions: kvalifikovati - kvalificirati
        mod_lemma_ovati = lemma[:-5]+"ovati"
        mod_lemma_isati = lemma[:-5]+"isati"
        makedicts("irati", "ovati", ir_ov_dict, irati_in_sr_dict, sr_lemma, hr_lemma,mod_lemma_ovati)
        makedicts("irati", "isati", ir_is_dict, irati_in_sr_dict, sr_lemma, hr_lemma,mod_lemma_isati)

    if lemma.startswith("k"):
        mod_lemma = lemma[0].replace('k','h')+lemma[1:]
        makedicts("k", "h", k_h_dict, k_in_sr_dict, sr_lemma, hr_lemma,mod_lemma)

    if lemma.startswith("h"):
        mod_lemma = lemma[1:]
        makedicts("h", "h-drop", h_drop_dict, no_h_drop_in_sr_dict, sr_lemma, hr_lemma,mod_lemma)

    if "eu" or "au" in lemma:
        mod_lemma = lemma.replace('eu','ev').replace("au", "av")
        makedicts("eu", "ev", diftong_v_dict, diftong_aueu_in_sr_dict, sr_lemma, hr_lemma,mod_lemma)

    if u"ć" in lemma:
        mod_lemma = lemma.replace(u'ć',u'št')
        makedicts("c", "st", st_c_dict, c_in_sr_dict, sr_lemma, hr_lemma,mod_lemma)


def writeinfile(mydict,myout):
    for token in sorted(mydict):
        myout.write(token.encode("utf8")+"\t"+mydict[token]+"\n")
    myout.close()
    return myout

def writediff(mydict, myout):
    for token in sorted(mydict):
        myout.write(token.encode("utf8")+"\n")
    myout.close()
    return myout

writeinfile(yat_dict,yat)
writeinfile(diftong_v_dict,diftong_v)
writeinfile(h_drop_dict,h_drop)
writeinfile(k_h_dict,k_h)
writeinfile(st_c_dict,st_c)
writeinfile(ir_is_dict,ir_is)
writeinfile(ir_ov_dict,ir_ov)


writediff(diftong_aueu_in_sr_dict,diftong_aueu_in_sr)
writediff(no_h_drop_in_sr_dict,no_h_drop_in_sr)
writediff(k_in_sr_dict,k_in_sr)
writediff(c_in_sr_dict,c_in_sr)
writediff(irati_in_sr_dict,irati_in_sr)

## eventually  for creating -ist lexicon (vizazist)
## problem: false positivs

#if tag == u"Ncmsn" and token.endswith(u"ist"):
#dia_token=remove_diacritics(token)
#if dia_token!=token:
#    ist.write(dia_token.encode('utf8')+'\n')
