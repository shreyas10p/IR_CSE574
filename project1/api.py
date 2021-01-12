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
# 'us economy coronavirus'  india hashtag


# searchtags_usa = ['covid19 trump policy','coronavirus economy america','america covid deaths','#BeatCOVID19 america','#StopTheSpread'
    # 'corona america','#wearamask america','corona shutdown us','covid daily cases us','covid19 masks usa','covid trump masks','coronavirus trump','federal government covid usa','coronavirus','covid19','trump masks','social distancing','global pandemic usa','#longcovid usa','lives lost covid usa','#StopTheSpread usa trump','unemployment trump','us economy covid','#COVID__19 trump','anti mask us officials','pandemic control trump','CDC lives lost']

# searchtags_usa = ['CDC masks usa','schools reopening covid usa','CDC guideline trump','covid response CDC','covid vaccine trump','covid testing trump','CDC testing','testing guidelines trump','covid rates usa','#CoronavirusOutbreak usa','covid tests usa']

# searchtags_usa = ['covid tests trump','#Publichealth usa','testing guidance trump','virus vaccine usa','trump vaccine','warp speed covid','pandemic good trump','pandemic bad trump','trump pandemic','fauci pandemic','fauci response','pandemic response trump','trump guidelines covid','trump health covid','trump tests covid','trump economy covid','doctors trump']
# 'health staff trump','GDP usa','GDP trump','covid recovery usa','covid immune test','covid data usa','covid president trump','fauci president trump','fauci trump','social distancing usa','quarantine usa','usa colleges covid'

# searchtags_india = ['lockdown india','#coronavirus modi','india policy covid','india covid deaths','india lockdown covid','india covid economy','india masks covid','लॉकडाउन नीति','व्यापार कोरोना','दुकानें कोरोना','कोविड सरकार','प्रवासी मजदूर कोरोना','कोरोना रेल गाड़ियों','अस्पताल कोरोना','चिकित्सक कोरोना','doctors कोरोना','nurses कोरोना','अस्पताल मौत कोरोना','रोज़गार अस्पताल','अस्पताल होटल कोरोना']
searchtags_india = ['सरकार अस्पताल','GDP भारत','vaccine modi','vaccine भारत सरकार','pmcares मोदी सरकार','विकास मोदी कोरोना','टेस्ट कोरोना','social distancing india','सोशल डिस्टन्सिंग','quarantine india','airport india']

# searchtags_india = ['कोरोना रोजगार भारत','कोरोना नीति सरकार','कोरोना मोदी','मास्क कोरोना','कोरोनावाइरस सरकार','महामारी कोरोना','लॉकडाउन कोरोना','कोरोना मौतें','testing कोरोना','परिक्षण कोरोना','कोरोना वॉरीअर','कोरोना बेरोजगारी सरकार','मोदी सरकार लॉकडाउन','कोरोना संक्रमण','नौकरियाँ कोरोना सरकार','असंगठित वर्ग कोरोना','कोविड बेरोजगारी','#विकास_गायब_है कोरोना','कोरोना को हरायेंगे','Do Gaj Ki Doori','ज्यादा टेस्ट कोरोना','#IndiaFightsCorona','pmcares corona','economy covid india','migrantworkers corona india','RahulGandhi corona','#BeatCOVID19 india','mahamari corona sarkar','coronavirus pmcares','covid bharat sarkar','corona sarkar','corona rozgar']


# searchtags_italy = ['corona italy','economia corona','economia covid','covid italy morta','coronavirus casi italy','covid italy lavori',
                     # 'corona governo','corona morta italy','italy lockdown','#coronavirus Giuseppe conte',
                     # 'corona confinamento','confinamento governo politica','corona politica','confinamento governo','covid politica italy','#scuole covid','covid governo','covid ministro','#scuola2020 covid','#Covid_19 ','covid Giuseppe','#covid #zingaretti','#covid salvini','conte covid','parlamentari covid','corona confinamento','vaccini covid','dimaio vaccino']
# searchtags_italy = ['coronavirus governa','mascherina governa','policia mascherina','#festamodena covid','medician covid','ospedale covid','dottori covid','infermiera covid','infermieri covid','morta covid ospedale','governo ospedale','#milano italy covid','coronavirusitalla','italy GDP','italy ']
searchtags_italy = ['COvid19italia governo','lockdown','#coronavirus italy','italy covid cases','italy corona students','italy schools','italy deaths covid','riduzione dei contatti','confinamento italy','confinamento aeroporto']


# searchtags_italy = []

UNTIL_DATE = '2020-09-22'
LANGUAGUE_USA = 'en'
LANGUAGUE_ITALY = 'it'
LANGUAGUE_INDIA = 'hi'

def fetch_tweets(country,tags_list):
    try:
        for hashtag in tags_list:
            print(hashtag)
            initIndex = 1
            count = 1
            next_res = None
            if(country == 'usa'):
                payload = {'q':'to:{} filter:replies'.format(hashtag[1]),'result_type':'recent','lang':LANGUAGUE_USA,'since_id':hashtag[0],'count':200,'tweet_mode':'extended'}
            elif(country == 'india'):
                payload = {'q':'to:{} filter:replies'.format(hashtag[1]),'result_type':'recent','lang':LANGUAGUE_INDIA,'since_id':hashtag[0],'count':200,'tweet_mode':'extended'}
            else:
                payload = {'q':'to:{} filter:replies'.format(hashtag[1]),'result_type':'recent','lang':LANGUAGUE_ITALY,'since_id':hashtag[0],'count':200,'tweet_mode':'extended'}
            while(initIndex == 1):
                print("requests..",hashtag)
                if(next_res is None):
                    response = requests.get(REACTION_URL,auth=oauth,params=payload)
                else:
                    response = requests.get(REACTION_URL+str(next_res),auth=oauth)
                print(response.status_code,response)
                if(response.status_code == 200):
                    result = response.json()
                    if(len(result['statuses']) == 0):
                        initIndex = 0
                    else:
                        print("writing...")
                        # fileName = '_'.join(hashtag.split())
                        with open('output/reactions/'+country+'/'+str(hashtag[1])+str(hashtag[0])+str(count)+'.json',"w",encoding='utf-8') as outfile:
                            outfile.write(json.dumps(result))

                        count+=1
                        meta = result['search_metadata']
                        next_res = meta['next_results']
                        if(count>2):
                            initIndex = 0
                        time.sleep(20)
                else:
                    print(response.status_code)
                    break
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


if __name__ == '__main__':
    # fetch_tweets('usa',searchtags_usa)
    # getCount('usa')
    # fetch_tweets('india',searchtags_india)
    # fetch_tweets('italy',searchtags_italy)
    # getCount('italy')
    # getCount('india')
    # getCount('italy')
    f = open('output/reactions/modified_italy_0.json', "r")
    tweets = f.read()
    tweets_json = json.loads(tweets)
    f.close()
    tweets_for_reply = []
    # print(tweets_json)
    tweets_json = tweets_json[0:300]
    for tweet in tweets_json:
        tweets_for_reply.append([str(tweet['id']),tweet['user']['screen_name']])
    print(tweets_for_reply)
    fetch_tweets('italy',tweets_for_reply)
