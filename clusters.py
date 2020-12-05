from elasticsearch import helpers, Elasticsearch
import pandas as pd
import json, requests
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

es = Elasticsearch()
es = es.indices.refresh(index='movies')
genres = set()
user_ids = 0

movies_df = pd.read_csv('movies.csv', index_col=['movieId'])
ratings_df = pd.read_csv('ratings.csv', index_col=['movieId'])

unique_genre = movies_df['genres'].str.split('|', expand=True)

user_ids = ratings_df['userId'].nunique()

print(user_ids)

for idx in unique_genre.index:
    for i in range(0, 10):
        if unique_genre[i][idx] != None:
            genres.add(unique_genre[i][idx])


#ratings_df.join(movies_df).drop(columns=['timestamp','title']).sort_values(['userId']).to_csv("data.csv")
data_file = pd.read_csv("data.csv")

data_file = data_file.assign(genres=data_file.genres.str.split(
    "|")).explode('genres', ignore_index=True)

#mean_file = pd.DataFrame()

#for id in range(1, user_ids):
#    for genre in genres:
#        genre_per_user = data_file.loc[(data_file['userId'] == id) & (
#            data_file['genres'] == genre)]
#        mean = genre_per_user["rating"].mean()
#        temp = pd.DataFrame(
#
#            {
#                'userId': [id],
#                'genre': [genre],
#                'mean': [mean]
#
#            }
#
#        )
#        mean_file = pd.concat([mean_file, temp], ignore_index=True)
#
#mean_file.dropna().to_csv("mean.csv") 
