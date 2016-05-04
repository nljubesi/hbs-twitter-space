#-*-coding:utf8-*-

# in remote server (r2d2.ifi.uzh.ch)
# create a list of all words with diacritics
# purpose: for approximating the nr of tweets with and without diacritics and users who write with or without diacritics
# too many false positivs

import gzip

dia=gzip.open('dia-lexicon.gz','w')

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}

for myfile in ['/apertium-hbs.hbs_HR_purist.mte.gz','/apertium-hbs.hbs_SR_purist.mte.gz']:
    for line in gzip.open(myfile):
      token,lemma,tag=line.decode('utf8').split('\t')[:3]
      if any(mydia in token for mydia in dia)==True:
          dia.write(token.encode("utf8"+"\n"))



