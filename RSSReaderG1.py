import feedparser
import schedule
import time
import spacy
import pymongo
import time

nlp = nlp = spacy.load('pt')


client = pymongo.MongoClient("mongodb://localhost:27017/")
rss = client["rss"]
news = rss["news"]

def get_ents(ents):
    result_ents = []
    for ent in ents:
        result_ents.append(str(ent))
    return result_ents

def get_obj(entries):
    list_object_to_insert = []
    for entry in entries:
        #print(nlp(entry.title).ents)
        if (news.find_one({"_id":str(entry.id)})) is None:
            list_object_to_insert.append({"_id": str(entry.id),
                         "extracted": get_ents(nlp(entry.title).ents),
                        "timestamp":time.time()})  
    return list_object_to_insert


def get_news():
    NewsFeed = feedparser.parse("http://g1.globo.com/dynamo/rss2.xml")
    entries = NewsFeed.entries
    save_objects = get_obj(entries)
    for obj in save_objects:
        news.insert_one(obj)
    print("Connected, found {} more news".format(len(save_objects)))

schedule.every(5).minutes.do(get_news)
while 1:
    schedule.run_pending()
    time.sleep(1)

