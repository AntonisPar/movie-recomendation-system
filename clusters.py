import json
import requests
import tkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from elasticsearch import helpers, Elasticsearch

es = Elasticsearch()
es = es.indices.refresh(index='movies')
genres = set()
user_ids = 0

movies_df = pd.read_csv('movies.csv', index_col=['movieId'])
ratings_df = pd.read_csv('ratings.csv', index_col=['movieId'])

unique_genre = movies_df['genres'].str.split('|', expand=True)

user_ids = ratings_df['userId'].nunique()


for idx in unique_genre.index:
    for i in range(0, 10):
        if unique_genre[i][idx] != None:
            genres.add(unique_genre[i][idx])

genres_dict = {}
for val, item in enumerate(genres):
    genres_dict[item] = val
#########################################################################


def create_mean_file():

    ratings_df.join(movies_df).drop(columns=['timestamp', 'title']).sort_values(
        ['userId']).to_csv("data.csv")
    data_file = pd.read_csv("data.csv")

    data_file = data_file.assign(genres=data_file.genres.str.split(
        "|")).explode('genres', ignore_index=True)

    mean_file = pd.DataFrame()

    for id in range(1, user_ids):
        for genre in genres:
            genre_per_user = data_file.loc[(data_file['userId'] == id) & (
                data_file['genres'] == genre)]
            mean = genre_per_user["rating"].mean()
            temp = pd.DataFrame(

                {
                    'userId': [id],
                    'genre': [genre],
                    'mean': [mean]

                }

            )
            mean_file = pd.concat([mean_file, temp], ignore_index=True)

    mean_file.dropna().to_csv("mean.csv")


###################################################################

def create_clusters():

    mean_file = pd.read_csv('mean.csv')
    #X,  = make_blobs(n_samples=1000, centers=3, n_features=2)
    kmean_df = pd.DataFrame(mean_file, columns=['userId', 'mean'])
    kmeans = KMeans(n_clusters=5)
    y = kmeans.fit_predict(kmean_df[['userId', 'mean']])
    kmean_df['Cluster'] = y
    print(kmean_df)
    kmean_df.to_csv("clustering.csv")
