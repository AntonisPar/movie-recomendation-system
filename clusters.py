from elasticsearch import helpers, Elasticsearch
import pandas as pd 
import requests
import json


es = Elasticsearch()
es = es.indices.refresh(index='movies')
genres = set()
user_ids = 0

movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')

res = movies_df['genres'].str.split('|',expand=True) 

for idx in ratings_df.index:
    if ratings_df['userId'][idx] != user_ids:
        user_ids += 1

print(user_ids)

for idx in res.index:
    for i in range(0,10):
        if res[i][idx] != None: 
            genres.add(res[i][idx]) 

for i in range(1,user_ids):
    for j in genres:
        movies_df.loc[(movies_df['genres']==i)]

