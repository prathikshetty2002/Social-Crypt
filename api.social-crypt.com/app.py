from flask import Flask
import os
import tweepy
from dotenv import load_dotenv
from flask import request,jsonify
import snscrape.modules.twitter as snstwitter
import requests


app = Flask(__name__)


@app.route('/twitter')
def index():
    query = "https://app.daily.dev/jayeshvp24"
    tweets = []
    for tweet in snstwitter.TwitterSearchScraper(query).get_items():
        obj = {
            "userid": tweet.id,
            "username":tweet.user.username,
            "retweet":tweet.retweetCount,
            "likecount" : tweet.likeCount,
            "hashtags" : tweet.hashtags,
        }
        tweets.append(obj)
        print(tweet.date)
        if(len(tweets) == 200):
            break
    return jsonify({'result':tweets})


from goose3 import Goose
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}
API_URL_PROP = "https://api-inference.huggingface.co/models/valurank/distilroberta-propaganda-2class"



def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def queryprop(payload):
	response = requests.post(API_URL_PROP, headers=headers, json=payload)
	return response.json()


@app.route('/news')
def news():
    url = 'https://blogs.jayeshvp24.dev/dive-into-web-design'
    goose = Goose()
    articles = goose.extract(url)
    output = query({
	"inputs":  articles.cleaned_text
    })
    print(output)
    
    return output[0]['summary_text']


@app.route('/propaganda')
def propaganda():
    url = 'https://www.newsweek.com/russia-ukraine-nazis-baltic-states-propaganda-1776075'
    goose = Goose()
    articles = goose.extract(url)
    output = queryprop({
	"inputs":  articles.cleaned_text[0:600]
    })
    
    num = str(output[0][0]['score'])
    return num

	



if __name__ == '__main__':
    app.run(debug=True)
