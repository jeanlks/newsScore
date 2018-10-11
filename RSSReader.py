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

def get_news(feed):
    NewsFeed = feedparser.parse(feed)
    entries = NewsFeed.entries
    save_objects = get_obj(entries)
    for obj in save_objects:
        news.insert_one(obj)
    print("Connected to feed {}, found {} more news".format(feed,len(save_objects)))
    
def run_all_feeds():
    feeds = ['http://noticias.r7.com/feed.xml',
             'http://g1.globo.com/dynamo/brasil/rss2.xml',
             'http://rss.home.uol.com.br/index.xml',
             'http://rss.tecmundo.com.br/feed']
    
    for feed in feeds:
        get_news(feed)
    

schedule.every(1).minutes.do(run_all_feeds)
while 1:
    schedule.run_pending()
    time.sleep(1)

