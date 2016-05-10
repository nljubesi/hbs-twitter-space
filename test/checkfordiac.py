import gzip
#-*-coding:utf8-*-



dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}
userdict={}
users_dia={}
users_no_dia={}
dia_counter=0
only_dia_user_counter=0
only_nodia_user_counter=0
dia_and_no_dia_user_counter={}

user_tweets={}


for line in gzip.open('hrsrTweets.gz'):
    tid,user,time,lang,lon,lat,text=line[:-1].decode('utf8').split('\t')
    if user not in user_tweets:
        user_tweets[user]=1
    else:
        user_tweets[user]+=1

    if any(mydia in text for mydia in dia)==True:
        dia_counter+=1
        users_dia[user]="dia"
    else:
        users_no_dia[user]="no dia"

for diauser in users_dia:
    if diauser not in users_no_dia:
        only_dia_user_counter+=1
    else:
        dia_and_no_dia_user_counter[diauser]=1

for nodiauser in users_no_dia:
    if nodiauser not in users_dia:
        only_nodia_user_counter+=1
    else:
        dia_and_no_dia_user_counter[nodiauser]=1


print "\nThere are ", dia_counter, "tweets with diacritics\n"
#There are 387992 tweets with diacritics (387992/1350101=28%)

print "\nThere are ", only_dia_user_counter, "users whose tweets always contains diacritics"
print "\nThere are ", only_nodia_user_counter, "users whose tweets never contains diacritics"
print "\nThere are ", len(dia_and_no_dia_user_counter), "users whose tweets sometimes contain diacritics and sometimes not\n"

#if not noise:
# words with dia/all words here



