
# coding: utf-8

# In[ ]:


import feedparser
import schedule
import time
import spacy
import pymongo
import time

nlp = nlp = spacy.load('pt')

#Connects to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
rss = client["rss"]
news = rss["news"]


#Function that extracts meaningful information about news titles
def get_extracted(title):
    caracteristicas = []
    #for token in title:
    #    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #         token.shape_, token.is_alpha, token.is_stop)
    for i in range(len(title)):
        token = title[i]
        #print("token {}".format(token))
        if token.dep_ in ["nsubj","obl","csubj","xcomp",
                          "conj","advcl","nsubj","nsubj:pass"
                          ,"nsubjpass", "verb","noun","ROOT",
                          "obj","nmod","nmod:npmod","nummod","amod","flat:name"]:
            caracteristicas.append(token.text)
    return caracteristicas

#Gets the list of objects parsed
def get_obj(entries):
    list_object_to_insert = []
    for entry in entries:
        #print(nlp(entry.title).ents)
        if (news.find_one({"_id":str(entry.id)})) is None:
            extracted_list = get_extracted(nlp(entry.title))
            extracted_str = (' ').join(extracted_list)
            list_object_to_insert.append({"_id": str(entry.id),
                         "extracted": extracted_list,
                         "extracted_str": extracted_str, 
                         "timestamp":time.time()})  
    return list_object_to_insert

#Get news from a feed and saves to database if does not exists
def get_news(feed):
    NewsFeed = feedparser.parse(feed)
    entries = NewsFeed.entries
    save_objects = get_obj(entries)
    for obj in save_objects:
        news.insert_one(obj)
    print("Connected to feed {}, found {} more news".format(feed,len(save_objects)))
    
#Run all feeds of informations
def run_all_feeds():
    feeds = ['http://noticias.r7.com/feed.xml',
             'http://g1.globo.com/dynamo/brasil/rss2.xml',
             'http://rss.home.uol.com.br/index.xml',
             'http://feeds.bbci.co.uk/portuguese/rss.xml',
             'https://www.correiobraziliense.com.br/rss/noticia/brasil/rss.xml',
             'https://www.correiobraziliense.com.br/rss/noticia/mundo/rss.xml',
             'http://g1.globo.com/dynamo/mundo/rss2.xml',
			 'http://g1.globo.com/dynamo/goias/rss2.xml']
    
    for feed in feeds:
        get_news(feed)

#Schedule a task for running every specified minutes
run_all_feeds()
schedule.every(5).minutes.do(run_all_feeds)
while 1:
    schedule.run_pending()
    time.sleep(1)

