from io import BytesIO
from flask import Flask, jsonify
import os
# import tweepy
from dotenv import load_dotenv
from flask import request,jsonify
import snscrape.modules.twitter as snstwitter
from snscrape.modules.twitter import TwitterSearchScraper, TwitterSearchScraperMode
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
import pandas as pd
# from flask import send_file
from flask import send_file
import datetime
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging
import sys
from llama_index import GPTVectorStoreIndex, TwitterTweetReader
import os
import llama_index
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

os.environ['OPENAI_API_KEY']='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'

app = Flask(__name__)

twitterData = None
queryString = None

# print(type(twitterData))

load_dotenv()

print(os.getenv("HUGGINGFACE_API"))

def runner():
	print("the code is shit")
	
@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

@app.route('/twitter')
def twitter():
    query = request.args['query']
    retweet = 0
    likecount = 0
    hashtags = set([])
    i=0
    global twitterData
    global queryString
    print("Url: Twitter, data: ", twitterData)
    print("Url: Twitter, query: ", queryString)
    # if twitterData is None:
    #     twitterData = snstwitter.TwitterSearchScraper(query).get_items()
    #     queryString = query
    # else:
    #     if queryString != query:
    #         twitterData = snstwitter.TwitterSearchScraper(query).get_items()
    #         queryString = query
    #     else:
    #         print(vars(twitterData)) 
    #         print("not scraping again")
    # twitter_scraper = TwitterSearchScraper(query)
    # twitterData = list(twitter_scraper.get_items(TwitterSearchScraperMode.TOP))
    twitterData = snstwitter.TwitterSearchScraper(query).get_items()
        
    for tweet in twitterData: 
        print("looping through tweets")
        print(vars(tweet)) 
        likecount += tweet.likeCount
        retweet += tweet.retweetCount + tweet.quoteCount
        if(tweet.hashtags != None):
            for h in tweet.hashtags:
                hashtags.add(h)
        
        i+= 1
        
        if(i==200):
            break
        
    tweets = {"likecount":likecount,"retweet":retweet,"hashtags":list(hashtags),"count":i}
    print(tweets)
    return jsonify({'result':tweets})


@app.route('/xyz')
def xyz():
    query = request.args['query']
    tweets = []
    for tweet in snstwitter.TwitterProfileScraper(query).get_items():
        tweets.append(tweet.date)
    return tweets



API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer " +  os.getenv('HUGGINGFACE_API') }
API_URL_PROP = "https://api-inference.huggingface.co/models/valurank/distilroberta-propaganda-2class"
API_URL_HATE = "https://api-inference.huggingface.co/models/IMSyPP/hate_speech_en"



def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def queryprop(payload):
	response = requests.post(API_URL_PROP, headers=headers, json=payload)
	return response.json()

def query_hate(payload):
	response = requests.post(API_URL_HATE, headers=headers, json=payload)
	return response.json()



@app.route('/sentiment')
def sentiment():
    query = request.args['query']
    retweet = 0
    likecount = 0
    hashtags = []
    senti=[]
    i=0
    positive=0
    negative=0
    neutral=0
    global twitterData
    global queryString
    print("Url: Sentiment, data: ", twitterData)
    # if twitterData is None:
    #     twitterData = snstwitter.TwitterSearchScraper(query).get_items()
    #     queryString = query
    # else:
    #     if queryString != query:
    #         twitterData = snstwitter.TwitterSearchScraper(query).get_items()
    #         queryString = query
    twitterData = snstwitter.TwitterSearchScraper(query).get_items()
        
    for tweet in twitterData: 
        if tweet.lang=="en":
            i+=1
            if(i==200):
                break
            sentence= tweet.rawContent
            print(sentence)
            sid_obj = SentimentIntensityAnalyzer()
            sentiment_dict = sid_obj.polarity_scores([sentence])
            print(sentiment_dict['neg']*100, "% Negative")
            print(sentiment_dict['pos']*100, "% Positive")
            print("Review Overall Analysis", end = " ") 
            if sentiment_dict['compound'] >= 0.05 :
                positive+=1
            elif sentiment_dict['compound'] <= -0.05 :
                negative+=1
            else :
                neutral+=1
    senti={"positive":positive, "negative":negative, "neutral":neutral}
    labels = list(senti.keys())
    values = list(senti.values())
        
    return {"labels":labels, "values":values}
            
@app.route('/sentiment_article')
def sentiment_article():
    senti=[]
    url = 'https://blogs.jayeshvp24.dev/dive-into-web-design'
    goose = Goose()
    articles = goose.extract(url)
    sentence1 = articles.cleaned_text
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores([sentence1])
    print(sentiment_dict['neg']*100, "% Negative")
    print(sentiment_dict['pos']*100, "% Positive")
    print("Review Overall Analysis", end = " ") 
    if sentiment_dict['compound'] >= 0.05 :
        senti.append("Positive")
    elif sentiment_dict['compound'] <= -0.05 :
        senti.append("Negative")
    else :
        senti.append("Neutral")
    return jsonify({"result":senti})



@app.route('/article-sentiment')
def articleSentiment():
    url = request.args['url']

    # url = 'https://blogs.jayeshvp24.dev/dive-into-web-design'
    goose = Goose()
    articles = goose.extract(url)
    sentence = articles.cleaned_text[0:500]
    print(sentence)
    output=query_hate({
	"inputs": str(sentence)})
    # print(output[0][0])
    result = {}
    for data in output[0]:
        if data['label'] == "LABEL_0":
            result["ACCEPTABLE"] = data['score']
        elif data['label'] == "LABEL_1":
            result["INAPPROAPRIATE"] = data['score']
        elif data['label'] == "LABEL_2":
            result["OFFENSIVE"] = data['score']
        elif data['label'] == "LABEL_3":
            result["VIOLENT"] = data['score']
    labels = list(result.keys())
    values = list(result.values())

    # # Use `hole` to create a donut-like pie chart
    # fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    # # fig.show()
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # print(graphJSON)
    # print(type(fig))
    # return graphJSON
    return jsonify({"labels": labels, "values": values})
            





@app.route('/summary')
def summary():
    try:

        url = request.args['url']
        goose = Goose()
        articles = goose.extract(url)
        output = query({
        "inputs":  articles.cleaned_text
        })
        print(output)
    except:
        return "Please put the relevant text article"

    return jsonify({"result": output[0]['summary_text']})

@app.route('/wordcloud')
def plotly_wordwordcloud():
    url = request.args['url']
    goose = Goose()
    articles = goose.extract(url)
    text = articles.cleaned_text
    wordcloud = WordCloud(width=1280, height=853, margin=0,
                      colormap='Blues').generate(text)
    wordcloud.to_file("./wordcloud.png")
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.margins(x=0, y=0)
    
    # plt.show()
    # img = BytesIO()

    # plt.savefig("./wordcloud.png", format='png')
    # plt.imsave("./wordcloud.png", format='png')
    # img.seek(0)
    # # nimg = Image.frombytes("RGBA", (128, 128), img, 'raw')
    # nimg = Image.frombuffer(img)
    # nimg.save("./wordcloud.png")
    # plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return send_file("./wordcloud.png", mimetype='image/png')
    # return render_template('plot.html', plot_url=plot_url)

# @app.route('/cloud')
# def plotly_wordcloud():
#     url = 'https://blogs.jayeshvp24.dev/dive-into-web-design'
#     goose = Goose()
#     articles = goose.extract(url)
#     text = query({
# 	"inputs":  articles.cleaned_text
#     })
#     wc = WordCloud(stopwords = set(STOPWORDS),
#                    max_words = 200,
#                    max_font_size = 100)
#     wc.generate(text[0]['summary_text'])
@app.route('/propaganda')
def propaganda():
    url = request.args['url']
    goose = Goose()
    articles = goose.extract(url)
    output = queryprop({
	"inputs":  articles.cleaned_text[0:600]
    })
    
    yes = output[0][0]['score']
    no = 1 - yes
    return jsonify({"yes": yes, "no": no})



@app.route("/chat", methods=["GET"])
def chat():
    # Get the query from the request body.
    query = request.args['url']
    # create an app in https://developer.twitter.com/en/apps
    # create reader, specify twitter handles
    reader = TwitterTweetReader(BEARER_TOKEN)
    documents = reader.load_data(["ANI"])
    # Create a new instance of the llama chatbot agent.
    agent = llama_index.GPTVectorStoreIndex.from_documents(documents)
    chat_engine = agent.as_chat_engine(verbose=True)

    # Get the response from the llama chatbot agent.
    response = chat_engine.chat(query)

    # Return the response as JSON.
    return jsonify({"response": response})

# @app.route('/cloud')
# def plotly_wordcloud():
#     url = request.args['url']
#     goose = Goose()
#     articles = goose.extract(url)
#     text = query({
# 	"inputs":  articles.cleaned_text
#     })
#     wc = WordCloud(stopwords = set(STOPWORDS),
#                    max_words = 200,
#                    max_font_size = 100)
#     wc.generate(text[0]['summary_text'])
    
#     word_list=[]
#     freq_list=[]
#     fontsize_list=[]
#     position_list=[]
#     orientation_list=[]
#     color_list=[]

#     for (word, freq), fontsize, position, orientation, color in wc.layout_:
#         word_list.append(word)
#         freq_list.append(freq)
#         fontsize_list.append(fontsize)
#         position_list.append(position)
#         orientation_list.append(orientation)
#         color_list.append(color)
        
#     # get the positions
#     x=[]
#     y=[]
#     for i in position_list:
#         x.append(i[0])
#         y.append(i[1])
            
#     # get the relative occurence frequencies
#     new_freq_list = []
#     for i in freq_list:
#         new_freq_list.append(i*100)
#     new_freq_list
    
#     trace = go.Scatter(x=x, 
#                        y=y, 
#                        textfont = dict(size=new_freq_list,
#                                        color=color_list),
#                        hoverinfo='text',
#                        hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
#                        mode='text',  
#                        text=word_list
#                       )
    
#     layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
#                         'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    
#     fig = go.Figure(data=[trace], layout=layout)
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     print(graphJSON)
#     print(type(fig))
#     return graphJSON

@app.route('/authenticity')
def auth():
    url = request.args['url']
    lis = []
    df = pd.read_csv('blacklist.csv')
    for i in range(len(df)):
        lis.append(df.loc[i, "MBFC"])

    for l in lis:
        if(url.__contains__(l)):
            return {"authentic":False}

    return { "authentic": True }

@app.route('/bot-activity')
def botActivity():
    url = request.args['url']
    i=0
    usernames = []
    time = []
    finalusername = []
    for tweet in snstwitter.TwitterSearchScraper(url).get_items():
        usernames.append(tweet.user.username)
        time.append(tweet.date)
        if(i==150):
            break
        i+=1

    flag = False
    for i in range(len(time)-1):
        a = time[i]
        b = time[i+1]
        c = a-b
        if(c.seconds <= 60):            
            finalusername.append(usernames[i+1])

    print("username: ", finalusername)
    if(len(finalusername) > 3):
        flag = True
    return jsonify({"bots":list(set(finalusername)),"flag":flag})
#baseline model
if __name__ == '__main__':
    app.run(debug=True)
