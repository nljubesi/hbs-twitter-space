#!/usr/bin/python
#-*-coding:utf8-*-

## Script for extracting customized dictionaries for the variables which are different in Serbian and Croation

import gzip

## Open files for storing custom. lexicons with words and their variables (word \t var)
lexicon_dirs='../../lexicons/apertium'
yat=gzip.open('../custom-lexicons/yat-lexicon.gz','w')
ir_is=gzip.open('../custom-lexicons/ir-is-lexicon.gz', 'w')
ir_ov=gzip.open('../custom-lexicons/ir-ov-lexicon.gz', 'w')
k_h=gzip.open('../custom-lexicons/kh-lexicon.gz','w')
h_drop=gzip.open('../custom-lexicons/hdrop-lexicon.gz','w')
st_c=gzip.open('../custom-lexicons/st-c-lexicon.gz','w')
diftong=gzip.open('../custom-lexicons/diftong-v-lexicon.gz','w')
kinja_ica=gzip.open('../custom-lexicons/kinja-ica-lexicon.gz', 'w')
ka_ica=gzip.open('../custom-lexicons/ka-ica-lexicon.gz', 'w')
lac_telj=gzip.open('../custom-lexicons/lac-telj-lexicon.gz', 'w')


## Open dicts for storing variables which will be written in output files (customized lexicons)
yat_dict, h_drop_dict, k_h_dict, st_c_dict, ir_is_dict, ir_ov_dict, diftong_dict, kinja_ica_dict, ka_ica_dict, lac_telj_dict \
    = {},{},{},{},{},{},{},{},{},{}


dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
"""Function for replacing diacritics with their diacrtitic-free equivalents"""
def remove_diacritics(token):
    result=''
    for char in token:
        result+=dia.get(char,char)
    return result

## Function for writing the files (customized dictionaries)
def writeinfile(mydict,myout):
    for token in sorted(mydict):
        myout.write(token.encode("utf8")+"\t"+mydict[token]+"\n")
    myout.close()
    return myout

## Lists for storing ambiguous words which would produce a lot of false positives
ambiguity = [u"reko", u"reci", u"njega"]
negation=[u"necu", u"neces", u"nece", u"necemo", u"necete"]
## Without this list:
## -reko/reci (VERB short for 'told'; VERB imperativ tell) would be marked as an opposition to rijeko (NOUN vocative river)
## -njega (PRON him) would be marked as an opposition to 'nega' (care)

## Open log file for storing candidate oppositions
log=open('log','w')
## Open dicts for storing tokens and their tags
hr={}
sr={}
## Open dicts for storing lemmas and their tokens
hr_lemma={}
sr_lemma={}

## For each line in HR apertium dict
for line in gzip.open(lexicon_dirs+'/hrLex_v1.0.gz'):
    ## Separate it by tabulator and define its memebers as token, lemma, pos-tag
    token,lemma,tag=line.decode('utf8').split('\t')[:3]
    token=token.lower()
    lemma=lemma.lower()
    #if token.lower()!=token:
    #    continue
    ## Store each token in hr dictionary where token is a key and it set of its tags is value
    if token not in hr:
        hr[token]=set()
    hr[token].add(tag)
    ## Store each lemma in hr dictionary where lemma is a key and it set of its tokens is value
    if lemma not in hr_lemma:
        hr_lemma[lemma]=set()
    #if lemma == "europa":
    #    print lemma
    hr_lemma[lemma].add(token)
log.write(repr(hr.items()[:10])+'\n')

## For each line in SR apertium dict
for line in gzip.open(lexicon_dirs+'/srLex_v1.0.gz'):
    ## Separate it by tabulator and define its memebers as token, lemma, pos-tag
    token,lemma,tag=line.decode('utf8').split('\t')[:3]
    #if token.lower()!=token:
    #    continue
    ## Store each token in hr dictionary where token is a key and it set of its tags is value
    token=token.lower()
    lemma=lemma.lower()
    if token not in sr:
        sr[token]=set()
    sr[token].add(tag)
    ## Store each lemma in hr dictionary where lemma is a key and it set of its tokens is value
    if lemma not in sr_lemma:
        sr_lemma[lemma]=set()
    sr_lemma[lemma].add(token)
log.write(repr(sr.items()[:10])+'\n')

## For each token in lexicon with HR tokens
for index,token in enumerate(hr):
    if index%100==0:
        log.write(str(index+1)+' od '+str(len(hr))+'\n')
    ## Replace the Ijekavian-jat reflex with Ekavian yat reflex
    ijee=token.replace('ije','e')
    jee=token.replace('je','e')
    ijej=token.replace('ij','ej')
    io=token.replace('io','eo')

    ## For each modified (replaced) token
    for mod_token in (ijee,jee,ijej,io):
        if token==mod_token:
            continue

        ## If token and mod_token are not in the list of ambiguos words (to avoid many false positivs)
        if mod_token not in ambiguity and token not in ambiguity:
        ## If modified token can be found in SR apertium dictionary
            if mod_token in sr:
                ## Mark is as a candidate SR opposition
                log.write(repr('candidate '+token+' '+mod_token)+'\n')
                ## If there Croatian token and Serbian candidate token share ad least one PoS Tag
                if len(hr[token].intersection(sr[mod_token]))>0:
                    ## If the Serbian candidate token is not present in HR apertium dictionary
                    if mod_token not in hr :
                        # Store the HR and SR tokens in the yat-dic with their respective variables
                        yat_dict[token]="je"
                        yat_dict[mod_token]="e"
                        ## Strip diactics from token and modified token
                        dia_token=remove_diacritics(token)
                        dia_mod_token=remove_diacritics(mod_token)
                        ## Since we stripped diacritics reči (not ambig) is now reci (ambig),
                        # and nečeš (not ambig.) is now neces (ambig) so we check once again for ambiguity
                        ## If the candidates are not in the list of ambiguity, store them in the yat-dict
                        if dia_mod_token not in negation and dia_mod_token not in ambiguity:
                            yat_dict[dia_mod_token]="e"
                            yat_dict[dia_token]="je"


    ## For the opposition k/h
    if "k" in token:
        ## Eliminate possible false positive (korov-horov i sve njihove varijacije)
        if not "korov" in token:
            mod_token=token.replace("k","h")
            if token==mod_token:
                continue
            ## If the Serbian candidate token is present in SR token dictionary
            if mod_token in sr:
                log.write(repr('candidate '+token+' '+mod_token)+'\n')
                if len(hr[token].intersection(sr[mod_token]))>0:
                    ## If the Serbian candidate token is not present in HR token dictionary, store it with its variable
                    if mod_token not in hr:
                        dia_token=remove_diacritics(token)
                        dia_mod_token=remove_diacritics(mod_token)
                        k_h_dict[token]="k"
                        k_h_dict[dia_token]="k"
                        k_h_dict[mod_token]="h"
                        k_h_dict[dia_mod_token]="h"

    ## For the opposition ć/št
    if u'ć' in token:
        ## Eliminate possible false positives (vec-vest, zakreciti-zakrestiti, i sve njihove varijacije)
        if not (token.startswith(u"već") or token.startswith(u"zakreć")):
            mod_token=token.replace(u'ć',u'št')
            ## If the Serbian candidate token is present in SR token dictionary
            if mod_token in sr:
                log.write(repr('candidate '+token+' '+mod_token)+'\n')
                if len(hr[token].intersection(sr[mod_token]))>0:
                    ## If the Serbian candidate token is not present in HR token dictionary, store it with its variable
                    if mod_token not in hr:
                        dia_token=remove_diacritics(token)
                        dia_mod_token=remove_diacritics(mod_token)
                        st_c_dict[token]="c"
                        st_c_dict[dia_token]="c"
                        st_c_dict[mod_token]="st"
                        st_c_dict[dia_mod_token]="st"
                    ## Adaptation to errors in apertium dictionary
                    ## If the Serbian candidate token is present in HR token dictionary, but it has another tag, store it with its variable
                    ## Example: uopšte is present in hr dict, but as a conj. of uopštiti
                    elif mod_token in hr:
                        if len(hr[mod_token].intersection(sr[mod_token]))==0:
                            dia_token=remove_diacritics(token)
                            dia_mod_token=remove_diacritics(mod_token)
                            st_c_dict[token]="c"
                            st_c_dict[dia_token]="c"
                            st_c_dict[mod_token]="st"
                            st_c_dict[dia_mod_token]="st"

    ## For the opposition h-drop/no-h-drop)
    if 'h' in token:
        ## Eliminate possible false positives
        if not (token.startswith("mlada") or token.startswith("hlep")):
            mod_token=token.replace('h','')
            ## If the Serbian candidate token is present in SR token dictionary
            if mod_token in sr:
                log.write(repr('candidate '+token+' '+mod_token)+'\n')
                if len(hr[token].intersection(sr[mod_token]))>0:
                    ## If the Serbian candidate token is not present in HR token dictionary, store it with its variable
                    if mod_token not in hr:
                        dia_token=remove_diacritics(token)
                        dia_mod_token=remove_diacritics(mod_token)
                        h_drop_dict[token]="no-h-drop"
                        h_drop_dict[dia_token]="no-h-drop"
                        h_drop_dict[mod_token]="h-drop"
                        h_drop_dict[dia_mod_token]="h-drop"


# Iterate over lemma-dictionaries for the oppositons irati-isati, irati-ovati, ica-kinja, ica-ka i ac-telj
# When iterating over the lemma-dictionaries we can check and replace the ending of a lemma and take all its tokens
# instead of cheching the ending of all its tokens (because it may produce a high nr of false positives)
# for each lemma in Croatian lemmas
for lemma in hr_lemma:

    ## Opposition irati-isati
    ## if the lemma ends with -irati
    if lemma.endswith("irati"):
        mod_lemma_isati = lemma[:-5]+"isati"
        ## Opposition irati-ovati
        if lemma.endswith("cirati"):
            ## deal with exceptions: kvalifikovati - kvalificirati
            mod_lemma_ovati = lemma[:-6]+"kovati"
        else:
            mod_lemma_ovati = lemma[:-5]+"ovati"
        ## If modified candidate lemma is in serbian-lemma-dict and if it is not in croatian-lemma-dict
        if mod_lemma_isati in sr_lemma and mod_lemma_isati not in hr_lemma:
            ## Get each token which has the Serbian lemma into a customized dict with token as key and variable as value
            for mysrtoken in sr_lemma[mod_lemma_isati]:
                dia_token = remove_diacritics(mysrtoken)
                ir_is_dict[mysrtoken]="isati"
                ir_is_dict[dia_token]="isati"
            ## Get each token which has the Croatian lemma into a customized dict with token as key and variable as value
            for myhrtoken in hr_lemma[lemma]:
                dia_token = remove_diacritics(myhrtoken)
                ir_is_dict[myhrtoken]="irati"
                ir_is_dict[dia_token]="irati"

        ## If modified candidate lemma is in serbian-lemma-dict and if it is not in croatian-lemma-dict
        if mod_lemma_ovati in sr_lemma and mod_lemma_ovati not in hr_lemma:
            ## Get each token which has the Serbian lemma into a customized dict with token as key and variable as value
            for mysrtoken in sr_lemma[mod_lemma_ovati]:
                dia_token = remove_diacritics(mysrtoken)
                ir_ov_dict[mysrtoken]="ovati"
                ir_ov_dict[dia_token]="ovati"
            ## Get each token which has the Croatian lemma into a customized dict with token as key and variable as value
            for myhrtoken in hr_lemma[lemma]:
                dia_token = remove_diacritics(myhrtoken)
                ir_ov_dict[myhrtoken]="irati"
                ir_ov_dict[dia_token]="irati"

    ## Oposition -ica/kinja
    if lemma.endswith("ica"):
        mod_lemma_kinja = lemma[:-3]+"kinja"

        ## If modified candidate lemma is in serbian-lemma-dict and if it is not in croatian-lemma-dict
        if mod_lemma_kinja in sr_lemma and mod_lemma_kinja not in hr_lemma:
            ## Get each token which has the Serbian lemma into a customized dict with token as key and variable as value
            for mysrtoken in sr_lemma[mod_lemma_kinja]:
                dia_token = remove_diacritics(mysrtoken)
                kinja_ica_dict[mysrtoken]="kinja"
                kinja_ica_dict[dia_token]="kinja"
            ## Get each token which has the Croatian lemma into a customized dict with token as key and variable as value
            for myhrtoken in hr_lemma[lemma]:
                dia_token = remove_diacritics(myhrtoken)
                kinja_ica_dict[myhrtoken]="ica"
                kinja_ica_dict[dia_token]="ica"


        ## Oposition -ica/ka
        # opravka/opravica ?
        if not lemma.startswith("oprav"):
            mod_lemma_ka = lemma[:-3]+"ka"
            ## If modified candidate lemma is in serbian-lemma-dict and if it is not in croatian-lemma-dict
            if mod_lemma_ka in sr_lemma and mod_lemma_ka not in hr_lemma:
                ## Get each token which has the Serbian lemma into a customized dict with token as key and variable as value
                for mysrtoken in sr_lemma[mod_lemma_ka]:
                    dia_token = remove_diacritics(mysrtoken)
                    ka_ica_dict[mysrtoken]="ka"
                    ka_ica_dict[dia_token]="ka"
                ## Get each token which has the Croatian lemma into a customized dict with token as key and variable as value
                for myhrtoken in hr_lemma[lemma]:
                    dia_token = remove_diacritics(myhrtoken)
                    ka_ica_dict[myhrtoken]="ica"
                    ka_ica_dict[dia_token]="ica"

    ## Oposition -telj/ac
    if lemma.endswith("telj"):
        mod_lemma = lemma[:-4]+"lac"
        ## If modified candidate lemma is in serbian-lemma-dict and if it is not in croatian-lemma-dict
        if mod_lemma in sr_lemma and mod_lemma not in hr_lemma:
            ## Get each token which has the Serbian lemma into a customized dict with token as key and variable as value
            for mysrtoken in sr_lemma[mod_lemma]:
                dia_token = remove_diacritics(mysrtoken)
                lac_telj_dict[mysrtoken]="lac"
                lac_telj_dict[dia_token]="lac"
            ## Get each token which has the Croatian lemma into a customized dict with token as key and variable as value
            for myhrtoken in hr_lemma[lemma]:
                dia_token = remove_diacritics(myhrtoken)
                lac_telj_dict[myhrtoken]="telj"
                lac_telj_dict[dia_token]="telj"

    if "eu" in lemma.lower():
        # avoid false positivs: neuredan-nevredan etc.
        if not ("ured" in lemma):
            mod_lemma = lemma.replace("eu", "ev")
            ## If modified candidate lemma is in serbian-lemma-dict and if it is not in croatian-lemma-dict
            if mod_lemma in sr_lemma and mod_lemma not in hr_lemma:
                ## Get each token which has the Serbian lemma into a customized dict with token as key and variable as value
                for mysrtoken in sr_lemma[mod_lemma]:
                    dia_token = remove_diacritics(mysrtoken)
                    diftong_dict[mysrtoken]="ev"
                    diftong_dict[dia_token]="ev"

                ## Get each token which has the Croatian lemma into a customized dict with token as key and variable as value
                for myhrtoken in hr_lemma[lemma]:
                    dia_token = remove_diacritics(myhrtoken)
                    diftong_dict[myhrtoken]="eu"
                    diftong_dict[dia_token]="eu"

# Since lemmas evropa/europa are in both apertium lexicons (and the conditions above would not recognize it as oppositions)
# , store them exceptionally in diftong_dict
if "evropa" in sr_lemma:
    for mysrtoken in sr_lemma["evropa"]:
        dia_token = remove_diacritics(mysrtoken)
        diftong_dict[mysrtoken]="ev"
        diftong_dict[dia_token]="ev"

if "europa" in hr_lemma:
    for mysrtoken in hr_lemma["europa"]:
        dia_token = remove_diacritics(mysrtoken)
        diftong_dict[mysrtoken]="eu"
        diftong_dict[dia_token]="eu"

writeinfile(yat_dict,yat)
writeinfile(ir_is_dict,ir_is)
writeinfile(ir_ov_dict,ir_ov)
writeinfile(k_h_dict,k_h)
writeinfile(h_drop_dict,h_drop)
writeinfile(st_c_dict,st_c)
writeinfile(diftong_dict,diftong)
writeinfile(kinja_ica_dict,kinja_ica)
writeinfile(ka_ica_dict,ka_ica)
writeinfile(lac_telj_dict,lac_telj)

