import json
from datetime import datetime, timedelta
import re
import demoji
from dateutil.parser import parse
import glob,os

#Remove Hashtags from full text
def remove_hashtags(string):
    string_array = string.split(' ')
    output_string = ''
    op_list = []
    for word in range(0, len(string_array)):
        try:
            if string_array[word].startswith('#') or '#' in string_array[word]:
                continue
            else:
                if string_array[word] not in op_list:
                    op_list.append(string_array[word])
        except IndexError as e:
            break
    for w in op_list:
        output_string = output_string + ' ' + w
    return output_string

#Remove Emoticons from full text : need to download emoticons
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    # list_emoji=demoji.findall(string)
    return emoji_pattern.sub(r'', string)

#Remove URL'S from full text
def remove_url(string):
    # text = re.sub(r'^http\s+?:\/\/.*[\r\n]*', '', string, flags=re.MULTILINE)
    text = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        " ", string)
    return text

#GET emoticons
def get_emoji_list(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)

    emoticons_dict = demoji.findall(string)
    if emoticons_dict is not None:
        emo_list = []
        for emo in emoticons_dict.keys():
            emo_list.append(emo)
    return emo_list

def remove_user_mentions(string):
    string_array = string.split(' ')
    output_string = ''
    op_list = []
    for word in range(0, len(string_array)):
        try:
            if string_array[word].startswith('@') or '@' in string_array[word]:
                continue
            else:
                if string_array[word] not in op_list:
                    op_list.append(string_array[word])
        except IndexError as e:
            break
    for w in op_list:
        output_string = output_string + ' ' + w
    return output_string


def get_hashtags(hashtags_li):
    return [hashtag['text'] for hashtag in hashtags_li]


def update_tweet(tweet,isPOI,country):
    if('text' in tweet):
        tweettext = tweet['text']
    else:
        tweettext = tweet['full_text']
    if (not tweet['retweeted']) and ('RT @' not in tweettext):
        if(isPOI):
            tweet['poi_name'] = tweet['user']['screen_name']
            tweet['poi_id'] = tweet['user']['id']
        else:
            tweet['poi_name'] = None
            tweet['poi_id'] = None
        tweet['country'] = country
        if('full_text' in tweet):
            tweet['tweet_text'] = tweet['full_text']
        elif('text' in tweet):
            tweet['tweet_text'] = tweet['text']
        tweet['tweet_lang'] = tweet.get('lang')
        full_text = tweet['tweet_text']
        removed_emoji_text = remove_emoji(full_text)
        removed_hashtags_text = remove_hashtags(removed_emoji_text)
        removed_url_text = remove_url(removed_hashtags_text)
        removed_all = remove_user_mentions(removed_url_text)
        if(tweet['tweet_lang'] == 'it'):
            tweet['text_it'] = removed_all.replace("RT","").replace("rt","")
        elif(tweet['tweet_lang'] == 'en'):
            tweet['text_en'] = removed_all.replace("RT","").replace("rt","")
        elif(tweet['tweet_lang'] == 'hi'):
            tweet['text_hi'] = removed_all.replace("RT","").replace("rt","")
        hashtags_list = get_hashtags(tweet['entities']['hashtags'])
        tweet['hashtags'] = hashtags_list
        tweet['mentions'] = [mention['screen_name'] for mention in tweet['entities']['user_mentions']]
        tweet['tweet_urls'] = [url['url'] for url in tweet['entities']['urls']]
        emoji_list  = get_emoji_list(full_text)
        tweet['tweet_emoticons'] = emoji_list
        date_str = parse(tweet['created_at'])
        time_obj = date_str.replace(second=0, microsecond=0, minute=0, hour=date_str.hour) + timedelta(hours=date_str.minute // 30)
        date_str = datetime.strftime(time_obj, '%Y-%m-%dT%H:%M:%SZ')
        tweet['tweet_date'] =date_str
        return tweet
    return None

def get_read_dir(country,isPOI):
    if(isPOI):
        os.chdir("output/POI/"+country)
    else:
        os.chdir("output/reactions/"+country)
    dir_list = []
    for file in glob.glob("*.json"):
        print(file)
        with open(file,'r',encoding='utf-8') as f:
            data = json.loads(f.read())
            for tweet in data['statuses']:
                updated_tweet = update_tweet(tweet,isPOI,country)
                if(updated_tweet is not None):
                    dir_list.append(updated_tweet)
    if(isPOI):
        with open("modified_"+country+".json","w+") as outfile:
            outfile.write(json.dumps(dir_list))
    else:
        with open("modified_"+str(country)+".json","w+") as outfile:
            outfile.write(json.dumps(dir_list))


def get_file_len(filepath):
    with open(filepath,'r') as outfile:
        data = json.loads(outfile.read())
    print(len(data))

def get_file():
    os.chdir("projfiles")
    all_data = []
    for file in glob.glob("*.json"):
        print(file)
        with open(file,'r',encoding='utf-8') as f:
            data = json.loads(f.read())
            for tweet in data:
                if(tweet['tweet_lang'] == 'it'):
                    tweet['text_it'] = tweet['text_it'].replace("RT","").replace("rt","")
                elif(tweet['tweet_lang'] == 'en'):
                    tweet['text_en'] = tweet['text_en'].replace("RT","").replace("rt","")
                elif(tweet['tweet_lang'] == 'hi'):
                    tweet['text_hi'] = tweet['text_hi'].replace("RT","").replace("rt","")
                all_data.append(tweet)
    with open("modified_.json","w+") as outfile:
        outfile.write(json.dumps(all_data))


if __name__ == '__main__':
    # get_read_dir('usa',isPOI = False)
    # get_file_len('output/reactions/usa/modified_usa.json')   #2631+5253
    # get_read_dir('italy',isPOI = False)
    # get_read_dir('usa',isPOI = False)
    # get_file_len('output/reactions/india/modified_india.json')    #3346 + 2517 + 8880
    # get_file_len('output/reactions/italy/modified_italy.json')   #2423 +1714
    get_file()
