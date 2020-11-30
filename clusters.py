from elasticsearch import helpers, Elasticsearch
import pandas as pd 
import requests
import json


es = Elasticsearch()
es = es.indices.refresh(index='movies')
genres = set()
user_ids = 0
mean=list()

movies_df = pd.read_csv('movies.csv',index_col=['movieId'])
ratings_df = pd.read_csv('ratings.csv',index_col=['movieId'])

res = movies_df['genres'].str.split('|',expand=True) 

user_ids=ratings_df['userId'].nunique()

print(user_ids)

for idx in res.index:
    for i in range(0,10):
        if res[i][idx] != None: 
            genres.add(res[i][idx]) 

#for i in range(1,user_ids):
#    for j in genres:
#        print(movies_df.loc[(movies_df['genres']==j)])


#ratings_df.join(movies_df).drop(columns=['timestamp','title']).sort_values(['userId']).to_csv("data.csv") 

data_file=pd.read_csv("data.csv")

#print(data_file)

data_file = data_file.assign(genres=data_file.genres.str.split("|")).explode('genres',ignore_index=True)

for id in range(1,user_ids):
    res1 = data_file.loc[(data_file['userId'] == id) & (data_file['genres'] == "Drama")] 
    print(res1)

#def calcMean(new_data):


