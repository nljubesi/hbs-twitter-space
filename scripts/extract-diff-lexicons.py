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

kinja_ica=gzip.open('../custom-lexicons/kinja-ica-lexicon.gz', 'w')
ka_ica=gzip.open('../custom-lexicons/ka-ica-lexicon.gz', 'w')
ac_telj=gzip.open('../custom-lexicons/lac-telj-lexicon.gz', 'w')

## To check the lexicons:
# diftong_aueu_in_sr=gzip.open('../../lexicons/eval-lexicons/diftong-aueu-in-sr.gz','w')
# no_h_drop_in_sr=gzip.open('../../lexicons/lexicons/eval-lexicons/no-h-drop-in-sr.gz','w')
# k_in_sr=gzip.open('../../lexicons/eval-lexicons/k-in-sr.gz','w')
# c_in_sr=gzip.open('../../lexicons/eval-lexicons/c-in-sr.gz','w')
# irati_in_sr=gzip.open('../../lexicons/eval-lexicons/irati-in-sr.gz','w')


## Open dicts for preventing duplicates
yat_dict, diftong_v_dict, h_drop_dict, k_h_dict, st_c_dict, ir_is_dict, ir_ov_dict, kinja_ica_dict, ka_ica_dict, ac_telj_dict \
    = {},{},{},{},{},{},{},{},{},{}

diftong_aueu_in_sr_dict, no_h_drop_in_sr_dict, k_in_sr_dict, c_in_sr_dict, irati_in_sr_dict, icakinja_in_sr_dict, icaka_in_sr_dict, telj_in_sr_dict \
    ={},{},{},{},{},{},{},{}


possible_fp = open("possible-fp", "w")

### up to date idea: ITERATE LEMMAS (not tokens)
# AND IF CONDITION FULLFILLED, TAKE THE TOKEN: LESS WORK TO DO & LESS SUBSTITUTIONS
### to be decided after talking with Nikola and Filip

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
def remove_diacritics(token):
    result=''
    for char in token:
        result+=dia.get(char,char)
    return result

some_possible_fp = [u"većina",u"veći",
                    u"neuredno",u"neuredan",u"neurednost",u"preuredan",
                   u"korist"]


negation=[u"necu", u"neces", u"nece", u"necemo", u"necete"]
e_ambiguity = [u"reko", u"reci"]
je_ambiguity = [u"njega"]
hlepe=[u"hlepjeti", u"hlepiti"]


def makedicts(hrout, srout, mydict, diffdict, srlemmadict, hrlemmadict,mod_lemma):

    # this condition would be neccessary, but serbian dicts also contain HR variations such as kaos etc.
    #if lemma not in srlemmadict:

    if mod_lemma in srlemmadict:
        # ex. if vest not in hr
        if mod_lemma not in hrlemmadict:
            # ex. for each declination of vest
            if lemma not in some_possible_fp:

                for mysrtoken in srlemmadict[mod_lemma]:
                    if mysrtoken not in hr:
                        dia_token = remove_diacritics(mysrtoken)
                        mydict[mysrtoken]=srout
                        mydict[dia_token]=srout
                for myhrtoken in hrlemmadict[lemma]:
                    if myhrtoken not in sr:
                        dia_token = remove_diacritics(myhrtoken)
                        mydict[myhrtoken]=hrout
                        mydict[dia_token]=hrout
                    else:
                        diffdict[myhrtoken]=1
            else:
                possible_fp.write(lemma.encode("utf8")+"\t"+mod_lemma.encode("utf8")+"\n")
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
# in SR standard there is also IJE/JE whereas other variables are not standard

for index,token in enumerate(hr):
    if index%100==0:
        log.write(str(index+1)+' od '+str(len(hr))+'\n')
    ijee=token.replace('ije','e')
    jee=token.replace('je','e')
    ijej=token.replace('ij','ej')
    io=token.replace('io','eo')

    for mod_token in (ijee,jee,ijej,io):
        if token==mod_token:
            continue
        if mod_token in sr:
            log.write(repr('candidate '+token+' '+mod_token)+'\n')
            if len(hr[token].intersection(sr[mod_token]))>0:
                if mod_token not in hr :
                    log.write('not in hr\n')
                    dia_token=remove_diacritics(token)
                    dia_mod_token=remove_diacritics(mod_token)
                    if token not in je_ambiguity:
                        yat_dict[token]="je"
                    if token not in e_ambiguity:
                        yat_dict[mod_token]="e"
                    if dia_token not in je_ambiguity:
                        yat_dict[dia_token]="je"

                    if dia_mod_token not in negation:
                        if dia_mod_token not in e_ambiguity:
                            yat_dict[dia_mod_token]="e"



for lemma in hr_lemma:

    if lemma.endswith("irati") and len(lemma)>7:

        mod_lemma_isati = lemma[:-5]+"isati"
        #exceptions: kvalifikovati - kvalificirati
        if lemma.endswith("cirati"):
            mod_lemma_ovati = lemma[:-6]+"kovati"
        else:
            mod_lemma_ovati = lemma[:-5]+"ovati"

        makedicts("irati-ov", "ovati", ir_ov_dict, irati_in_sr_dict, sr_lemma, hr_lemma,mod_lemma_ovati)
        makedicts("irati-is", "isati", ir_is_dict, irati_in_sr_dict, sr_lemma, hr_lemma,mod_lemma_isati)

    if lemma.startswith("k"):
        mod_lemma = lemma[0].replace('k','h')+lemma[1:]
        makedicts("k", "h", k_h_dict, k_in_sr_dict, sr_lemma, hr_lemma, mod_lemma)

    if lemma.startswith("h"):
        if not lemma in hlepe:
            mod_lemma = lemma[1:]
            makedicts("no-h-drop", "h-drop", h_drop_dict, no_h_drop_in_sr_dict, sr_lemma, hr_lemma, mod_lemma)

    if "eu" or "au" in lemma:
        mod_lemma = lemma.replace('eu','ev').replace("au", "av")
        makedicts("eu", "ev", diftong_v_dict, diftong_aueu_in_sr_dict, sr_lemma, hr_lemma, mod_lemma)

    if u"ć" in lemma:
        mod_lemma = lemma.replace(u'ć',u'št')
        makedicts("c", "st", st_c_dict, c_in_sr_dict, sr_lemma, hr_lemma, mod_lemma)

    if lemma.endswith("ica"):
        mod_lemma = lemma[:-3]+"kinja"
        makedicts("ica", "kinja", kinja_ica_dict, icakinja_in_sr_dict, sr_lemma, hr_lemma, mod_lemma)

    if lemma.endswith("ica"):
        mod_lemma = lemma[:-3]+"ka"
        makedicts("ica", "ka", ka_ica_dict, icaka_in_sr_dict, sr_lemma, hr_lemma, mod_lemma)

    if lemma.endswith("telj"):
        mod_lemma = lemma[:-3]+"lac"
        makedicts("telj", "lac", ac_telj_dict, telj_in_sr_dict, sr_lemma, hr_lemma, mod_lemma)

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

writeinfile(kinja_ica_dict,kinja_ica)
writeinfile(ka_ica_dict,ka_ica)
writeinfile(ac_telj_dict,ac_telj)


## To check the lexicons (what does not belong in which lexicon):

#writediff(diftong_aueu_in_sr_dict,diftong_aueu_in_sr)
#writediff(no_h_drop_in_sr_dict,no_h_drop_in_sr)
#writediff(k_in_sr_dict,k_in_sr)
#writediff(c_in_sr_dict,c_in_sr)
#writediff(irati_in_sr_dict,irati_in_sr)

