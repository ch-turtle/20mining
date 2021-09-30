import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["articles"]

d = datetime.utcnow().isoformat()[:-3]+'Z'

myquery = { "published": { "$gt": d }}
mydocs = mycol.find(myquery)
