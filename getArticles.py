#!/usr/bin/env python3
import feedparser
from pandas import json_normalize
import pandas as pd
import requests
import pymongo
import datetime


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["20mining"]

rss_url='https://partner-feeds.20min.ch/rss/20minuten'
art_url = 'https://feed-prod.unitycms.io/6/content/'


d = datetime.datetime.now()

# Read feed xml data
news_feed = feedparser.parse(rss_url) 

# Flatten data
df_news_feed=json_normalize(news_feed.entries)

# Read articles links
df_news_feed.link.head()

urls = df_news_feed['link'].values

for i in urls:
    id = i.split("/")[3]
    story = { "_id": id, "crawl": 0, "time": d}
    # If new article id: write to db and safe article, else pass
    try:
    	stories = mydb["stories"]
    	stories.insert_one(story)
    	articles = mydb["articles"]
    	r = requests.get(art_url+id)
    	r.encoding = 'utf-8'
    	articles.insert_one(r.json())
    except:
        continue
