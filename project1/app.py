import requests
import json
from dotenv import load_dotenv
import os
from requests_oauthlib import OAuth1
import traceback
import time
import glob
import tweepy
import time

load_dotenv(dotenv_path='credentials.env')

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TOKEN")
TOKEN_SECRET = os.getenv("TOKEN_SECRET")

oauth = OAuth1(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,TOKEN_SECRET)

USER_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
REACTION_URL = 'https://api.twitter.com/1.1/search/tweets.json'

def connect_to_twitter():
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    access_key = ACCESS_TOKEN
    access_secret = TOKEN_SECRET
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api


screen_name_india = ['drharshvardhan','mygovindia','ShashiTharoor']
screen_name_italy = ['matteosalvinimi','GiorgiaMeloni','matteorenzi']
screen_name_usa = ['Surgeon_General','SecPompeo','CDCgov']
poi_list=[screen_name_italy,screen_name_usa,screen_name_india]

searchtags_hindi = ['RahulGandhi corona','COVIDNewsByMIB corona','#BeatCOVID19 india','#coronavirus india']

searchtags_italy = ['corona italy','economia corona governo','economia italy covid','corona italy morta','coronavirus casi italy','covid italy lavori',
                    'corona governo','corona morta italy','italy lockdown','#coronavirus Giuseppe conte',
                    'corona confinamento','confinamento governo politica','corona politica','confinamento governo','covid politica italy']

searchtags_italy = ['covid government italy','coronavirus automobile','coronavirus italy','confinamento','confinamento salvini','covid lockdown',
    'jobs corona','economy corona']

searchtags_italy = ['#BeatCOVID19 governo','#StopTheSpread italy','#StayAtHome italy']

searchtags_usa = ['us economy coronavirus','trump coronavirus','covid19 trump','coronavirus economy usa','usa lockdown','usa covid testing','usa corona deaths',
    'corona industry us','corona shutdown us','covid daily cases us','covid19 masks usa','covid trump masks','coronavirus trump','federal government covid us']


searchtags1_usa = ['#BeatCOVID19','#StopTheSpread trump','#StayAtHome covid trump','#coronavirus']

searchtags_english = ['#coronavirus modi',
                    '#coronavirus jobs india','lockdown india','corona lockdown india']

searchtags_all = [searchtags1_usa]

def getPOItweets():
    max_id = None
    try:
        for country_poi in poi_list:
            for name in country_poi:
                count = 0
                for i in range(6):
                    if(i==0):
                        payload = {'screen_name':name,'tweet_mode':'extended','count':150}
                    else:
                        payload = {'screen_name':name,'tweet_mode':'extended','count':150,'max_id':max_id}
                    print("awaiting response...",payload)
                    response = requests.get(USER_URL,auth=oauth,params=payload)
                    print(response,"Response received.")
                    if(response.status_code==200):
                        result = response.json()
                        print(result)
                        max_id = result[-1]["id"]
                        print("writing...")
                        with open('output/POI/'+str(name)+'_'+str(i)+'.json',"w",encoding='utf-8') as outfile:
                            outfile.write(json.dumps(result))
                        print("writing done.")
                        # max_id = result[-1]["id"]
                    else:
                        break
                time.sleep(900)
    except:
        traceback.print_exc()

def getReactions():
    # os.chdir("output/reactions/"+country)
    initIndex = 1
    try:
        for tags in searchtags_all:
            for hashtag in tags:
                if(initIndex == 0):
                    payload = {'q':hashtag,'result_type':'recent','lang':'en',
                            'count':100,'tweet_mode':'extended','until':'2020-09-10'}
                else:
                    payload = {'q':hashtag,'result_type':'recent','lang':'en',
                            'count':100,'tweet_mode':'extended','until':'2020-09-10'}
                print("awaiting response...",payload)
                response = requests.get(REACTION_URL,auth=oauth,params=payload)
                print(response,"Response received.")
                if(response.status_code == 200):
                    result = response.json()
                    print(result)
                    print("writing...")
                    fileName = '_'.join(hashtag.split())
                    with open('/'+str(fileName)+''+str(initIndex)+'.json',"w",encoding='utf-8') as outfile:
                        outfile.write(json.dumps(result))
                    print("writing done.")
                else:
                    break
                time.sleep(100)
            initIndex = initIndex^1
            # time.sleep(1000)
    except:
        traceback.print_exc()


def getCount(country):
    os.chdir("output/reactions/"+country)
    count = 0
    for file in glob.glob("*.json"):
        print(file)
        with open(file,'r',encoding='utf-8') as f:
            data = json.loads(f.read())
        count+=len(data['statuses'])
    print(count)


def getReaction(country):
    os.chdir("output/reactions/"+country)
    count = 0
    # payload = {'q':hashtag,'result_type':'recent','lang':'en',
    #                         'count':100,'tweet_mode':'extended','until':'2020-09-10'}
    for file in glob.glob("*.json"):
        print(file)
        with open(file,'r',encoding='utf-8') as f:
            data = json.loads(f.read())
            meta = data.get('search_metadata',None)
            if(meta):
                next_res = meta.get('next_results',None)
                if(next_res):
                    response = requests.get(REACTION_URL+str(next_res),auth=oauth)
                    print(response,"Response received.")
                    if(response.status_code == 200):
                        result = response.json()
                        print(result)
                        print("writing...")
                        # fileName = '_'.join(hashtag.split())
                        with open('../../../usa/next_'+str(file),"w",encoding='utf-8') as outfile:
                            outfile.write(json.dumps(result))
                        print("writing done.")
                    else:
                        break
                    time.sleep(100)



def check_tweet_replies_length(tweet_replies_dict):
    cond_fulfilled = False
    for tweet_id in tweet_replies_dict.keys():
        if len(tweet_replies_dict[tweet_id]) >= 150:
            cond_fulfilled = True
        else:
            cond_fulfilled = False
            break
    return cond_fulfilled


def get_replies(filename):
    api = connect_to_twitter()

    f = open('output/reactions/' + filename + '.json', "r")
    tweets = f.read()
    tweets_json = json.loads(tweets)
    f.close()
    tweets_for_reply = []
    # print(tweets_json)
    tweets_json = tweets_json[:50]
    for tweet in tweets_json:
        tweets_for_reply.append([str(tweet['id']),tweet['user']['screen_name']])
    # print(tweets_for_reply)

    tweets_for_reply.sort(reverse=True)
    replies = {}
    # print("tweet count for reply: %d", count)

    count = 0
    # print("a",tweets_json)
    for t_id in tweets_for_reply:
        if count == 0:
            tweet_replies = tweepy.Cursor(api.search, q='to:{} filter:replies'.format(t_id[1]), sinceId=t_id[0],
                                          tweet_mode='extended').items(300)
        else:
            tweet_replies = tweepy.Cursor(api.search, q='to:{} filter:replies'.format(t_id[1]), sinceId=t_id[0],
                                          max_id=prev - 1, tweet_mode='extended').items(300)

        while True:
            try:
                reply = tweet_replies.next()
                if hasattr(reply, 'in_reply_to_status_id_str'):
                    if reply.in_reply_to_status_id_str in replies:
                        if check_tweet_replies_length(replies) or len(replies[t_id[0]]) >= 100:
                            break
                        replies[reply.in_reply_to_status_id_str].append(reply._json)
                    elif reply.in_reply_to_status_id_str in tweets_for_reply:
                        replies[reply.in_reply_to_status_id_str] = [reply._json]

            except tweepy.RateLimitError as e:
                print("--------------- Rate Limit Exceeded --------------")
                print(e)
                time.sleep(60 * 15)
                print("--------------- Start Processing --------------")
                continue

            except tweepy.TweepError as e:
                print("--------------- Tweep Error --------------")
                print(e)
                time.sleep(60 * 15)
                print("--------------- Start Processing --------------")
                continue

            except Exception as e:
                print(e)
                break

        count = count + 1
        prev = int(t_id[0])
        if check_tweet_replies_length(replies):
            break

    # print(replies)
    return replies


def store_tweets(alltweets, filename):
    op = json.dumps(alltweets)
    with open(filename + ".json", 'w+') as f1:
        f1.write(op)

if __name__ == "__main__":
    print("here")
    replies = get_replies('india/modified_india')
    store_tweets(replies,'replies_india')
    # getPOItweets()
    # getReactions()
    # getReaction('usa')
    # getCount('usa')
