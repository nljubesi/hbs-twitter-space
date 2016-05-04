
import gzip

user_tweets={}

for line in gzip.open('hrsrTweets.gz'):
    tid,user,time,lang,lon,lat,text=line[:-1].decode('utf8').split('\t')
    if user not in user_tweets:
        user_tweets[user]=1
    else:
        user_tweets[user]+=1

for myuser in sorted(user_tweets, key=user_tweets.get, reverse=True):
    #c+=1
    print myuser, "\t", user_tweets[myuser]