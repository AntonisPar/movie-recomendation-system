#from readCSV import uploadData
from elasticsearch import helpers, Elasticsearch
import pandas as pd 
import requests
import json

es = Elasticsearch() #CONNECT TO ELASTICSEARCH.
es.indices.refresh(index="movies") 
url = 'http://localhost:9200/movies/_doc/_search'
df = pd.read_csv('ratings.csv')
queryRes  = {}
ratingRes = {}
new_score = {} 

print("Please insert your User ID: ")
uID = int(input())



query = {
    "query": {
        "match": {
            # search against the 'title' field
            'title': str(input())
        }
    }
} 

def search(myQuery):
    res = requests.get(url, data=json.dumps(query), headers={'Content-Type': 'application/json'}) 
    search_hits = json.loads(res.text)['hits']['hits']

    pdres = df.loc[ (df['userId'] == uID)] 
    for index in pdres.index:
        ratingRes[int(pdres['movieId'][index])]= float(pdres['rating'][index])

    for hit in search_hits: 
        pdmean = df.loc[ (df['movieId'] == int(hit['_source']['movieId']))] 
        mean = 0
        base = 0

        for i in pdmean.index:
            mean = mean + float(pdmean['rating'][i])
            base = base + 1

        if int(hit['_source']['movieId']) in ratingRes:
            score = 0.25*float(hit['_score'])+0.5*ratingRes[int(hit['_source']['movieId'])] + 0.25*(mean/base)
            new_score[hit['_source']['title']] = score

        else: 
            score = 0.25*hit['_score'] + 0.25*(mean/base)
            new_score[hit['_source']['title']] = score

    sort_orders = sorted(new_score.items(), key=lambda x: x[1], reverse=True)

    print('Relevance Score\t Title') 
    for i in sort_orders:
        print("%.6f" % i[1],'\t' ,i[0])

search(query) 
