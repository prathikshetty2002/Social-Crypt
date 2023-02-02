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
    print(type(fig))
    return render_template(fig)


if __name__ == '__main__':
    app.run(debug=True)
