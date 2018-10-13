
# coding: utf-8

# In[1]:


import pymongo
import spacy
import operator

nlp = nlp = spacy.load('pt')

#Connects to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
rss = client["rss"]
news = rss["news"]


# In[2]:


def jaccard_distance(a, b):
    """Calculate the jaccard distance between sets A and B"""
    a = set(a)
    b = set(b)
    return 1.0 * len(a&b)/len(a|b)


# In[3]:


def getScoreNews():
    news_list = []
    for doc in news.find():
        news_list.append(doc)
        
    news_qnt = len(news_list)
    scores = {}
    i =0
    while (i<news_qnt-1):
        j = 0
        while(j<news_qnt-1):
            doc1 = news_list[i]['extracted_str']
            doc2 = news_list[j]['extracted_str']
           #print(doc1.similarity(doc2))
           # print('sentenca1: {} sentenca2: {}'.format(news_list[i]['extracted_str'], news_list[i+1]['extracted_str']))
            distance = jaccard_distance(doc1,doc2) 
            if distance > 0.80 and distance < 1.0 :
                print('sentenca1: {} sentenca2: {}'.format(doc1,doc2))
                if news_list[i]['link'] in scores:
                    scores[news_list[i]['link']] =  scores[news_list[i]['link']] + 1
                    del news_list[j]
                else:
                    scores[news_list[i]['_id']] = 1
                    del news_list[j]
            j = j+1
            news_qnt = len(news_list)
        i = i + 1
        #print('valor i: {} valor qnt: {}'.format(i, news_qnt))
    
    scores_sorted = s = [(k, scores[k]) for k in sorted(scores, key=scores.get, reverse=True)]
    
    for k, v in scores_sorted:
        print('link: {} n vzs:{}'.format(k,v))


# In[4]:


getScoreNews()


# In[5]:


jaccard_distance('HPV descoberta científica que milhões pessoas do vírus transmissível comum','HPV descoberta científica que milhões pessoas vírus sexualmente transmissível comum')

