from flask import Flask
import os
import tweepy
from dotenv import load_dotenv
from flask import request,jsonify
import snscrape.modules.twitter as snstwitter
import pandas as pd


app = Flask(__name__)


# @app.route('/twitter')
# def hello_world():
#     consumer_key = os.environ["API_KEY"]
#     consumer_secret = os.environ["API_KEY_SECRET"]
#     access_token = os.environ["ACCESS_TOKEN"]
#     access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
#     bearer_token = os.environ["BEARER_TOKEN"]

#     # client = tweepy.Client(
#     #     consumer_key,
#     #     consumer_secret,
#     #     access_token,
#     #     access_token_secret
#     # )
#     client = tweepy.Client(consumer_key= consumer_key,consumer_secret= consumer_secret,access_token= access_token,access_token_secret= access_token_secret)
#     query = 'news'
#     tweets = client.search_recent_tweets(query=query, max_results=10)
#     for tweet in tweets.data:
#         print(tweet.text)
#         # print(client.get_users_tweets("JayeshVP24"))
#         print(client.search_recent_tweets("nextjs"))

#         # auth = tweepy.OAuth1UserHandler(
#     #     consumer_key,
#     #     consumer_secret,
#     #     access_token,
#     #     access_token_secret
#     # )

#     # api = tweepy.API(auth)
#     # id = request.args['id']

#     # tweets = api.search_tweets(id, tweet_mode="extended")
#     # for tweet in tweets:
#     #     try:
#     #         print(tweet..full_text)
#     #         print("=====")
#     #     except AttributeError:
#     #         print(tweet.full_text)
#     #         print("=====")
    # return "Hello"


@app.route('/twitter')
def index():
    query = "https://www.rt.com/russia/551440-ukraine-us-financed-biolaboratories/"
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
        if(len(tweets) == 200):
            break
        print(len(tweets))
    return jsonify({'result':tweets})


from goose3 import Goose
@app.route('/news')
def news():
    url = 'https://blogs.jayeshvp24.dev/dive-into-web-design'
    goose = Goose()
    articles = goose.extract(url)
    return articles.cleaned_text

if __name__ == '__main__':
    app.run(debug=True)
