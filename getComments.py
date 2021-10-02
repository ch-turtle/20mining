import pymongo
from datetime import datetime, timedelta
import requests

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["20mining"]
stories = mydb["stories"]
comments = mydb["comments"]

com_url= 'https://api.20min.ch/comment/v1/comments?tenantId=6&contentId='


d = datetime.now()
print(d-timedelta(minutes = 5))

myquery = {
        '$or' : [
        {"$and": [ {"time": {"$lte": d-timedelta(minutes = 5)} }, { "crawl": 0 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(minutes = 10)} }, { "crawl": 1 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(minutes = 30)} }, { "crawl": 2 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(hours = 1)} }, { "crawl": 3 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(hours = 2)} }, { "crawl": 4 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(hours = 4)} }, { "crawl": 5 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(hours = 8)} }, { "crawl": 6 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(days = 1)} }, { "crawl": 7 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(days = 2)} }, { "crawl": 8 } ] },
        {"$and": [ {"time": {"$lte": d-timedelta(days = 7)} }, { "crawl": 9 } ] }
        ]
    }
    

mydocs = stories.find(myquery)

for x in mydocs:
    # Get Comments
    r = requests.get(com_url+x['_id']+'&limit=2000')
    r.encoding = 'utf-8'
    comments.insert_one(r.json())




    # Update Crawlcounter
    stories.update_one({"_id": x['_id']},{"$set": {"crawl": x["crawl"]+1}})
    
