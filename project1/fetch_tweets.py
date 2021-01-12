import requests
import json
from dotenv import load_dotenv
import os
from requests_oauthlib import OAuth1
import traceback
import time
import glob

load_dotenv(dotenv_path='credentials.env')

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TOKEN")
TOKEN_SECRET = os.getenv("TOKEN_SECRET")

oauth = OAuth1(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,TOKEN_SECRET)

USER_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
REACTION_URL = 'https://api.twitter.com/1.1/search/tweets.json'

UNTIL_DATE = '2020-09-18'

searchtags_india = []


def fetch_tweets(country,tags_list):
    try:
        for hashtag in tags_list:
            initIndex = 1
            count = 1
            next_res = None
            if(country == 'usa'):
                payload = {'q':hashtag,'result_type':'recent','lang':'en',
                        'count':200,'tweet_mode':'extended','until':'2020-09-20'}
            elif(country == 'india'):
                payload = {'q':hashtag,'result_type':'recent','lang':'hi',
                        'count':200,'tweet_mode':'extended','until':'2020-09-20'}
            else:
                payload = {'q':hashtag,'result_type':'recent','lang':'it',
                        'count':200,'tweet_mode':'extended','until':'2020-09-20'}
            while(initIndex == 1):
                print("requests..")
                if(next_res is None):
                    response = requests.get(REACTION_URL,auth=oauth,params=payload)
                else:
                    response = requests.get(REACTION_URL+str(next_res),auth=oauth)
                if(response.status_code == 200):
                    result = response.json()
                    if(len(result['statuses']) == 0):
                        initIndex = 0
                    else:
                        print("writing...")
                        fileName = '_'.join(hashtag.split())
                        with open('output/reactions/'+country+'/'+str(fileName)+''+str(count)+'.json',"w",encoding='utf-8') as outfile:
                            outfile.write(json.dumps(result))

                        count+=1
                        meta = result['search_metadata']
                        next_res = meta['next_results']
                        if(count>7):
                            initIndex = 0
                        time.sleep(30)
                else:
                    print(response.status_code)
                    break
    except:
        traceback.print_exc()

if __name__ == '__main__':
    fetch_tweets('india',searchtags_india)
