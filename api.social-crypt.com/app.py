from io import BytesIO
from flask import Flask 
import os
import tweepy
from dotenv import load_dotenv
from flask import request,jsonify
import snscrape.modules.twitter as snstwitter
import requests
from goose3 import Goose
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objs as go
import json
import plotly
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import base64
# from flask import send_file
from flask import send_file

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



API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
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

@app.route('/cloud2')
def plotly_wordcloud2():
    url = 'https://blogs.jayeshvp24.dev/dive-into-web-design'
    goose = Goose()
    articles = goose.extract(url)
    text = articles.cleaned_text
    wordcloud = WordCloud(width=1280, height=853, margin=0,
                      colormap='Blues').generate(text)
    wordcloud.to_file("./wordcloud.png")
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.margins(x=0, y=0)
    # # plt.show()
    # # img = BytesIO()

    # plt.savefig("./wordcloud.png", format='png')
    # plt.imsave("./wordcloud.png", format='png')
    # img.seek(0)
    # # nimg = Image.frombytes("RGBA", (128, 128), img, 'raw')
    # nimg = Image.frombuffer(img)
    # nimg.save("./wordcloud.png")
    # plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return send_file("./wordcloud.png", mimetype='image/png')
    # return render_template('plot.html', plot_url=plot_url)

@app.route('/cloud')
def plotly_wordcloud():
    url = 'https://blogs.jayeshvp24.dev/dive-into-web-design'
    goose = Goose()
    articles = goose.extract(url)
    text = query({
	"inputs":  articles.cleaned_text
    })
    wc = WordCloud(stopwords = set(STOPWORDS),
                   max_words = 200,
                   max_font_size = 100)
    wc.generate(text[0]['summary_text'])
    
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list
    
    trace = go.Scatter(x=x, 
                       y=y, 
                       textfont = dict(size=new_freq_list,
                                       color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode='text',  
                       text=word_list
                      )
    
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    
    fig = go.Figure(data=[trace], layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(graphJSON)
    print(type(fig))
    return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
