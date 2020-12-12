import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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

genres = sorted(genres)

#########################################################################


def create_mean_file():

    ratings_df.join(movies_df).drop(columns=['timestamp', 'title']).sort_values(
        ['userId']).to_csv("data.csv")
    data_file = pd.read_csv("data.csv")

    data_file = data_file.assign(genres=data_file.genres.str.split(
        "|")).explode('genres', ignore_index=True)

    mean_file = pd.DataFrame(columns=['userId'])
    for genre in genres:

        mean_file[str(genre)] = 0

    for id in range(1, user_ids+1):
        per_user_means = {"userId": id}
        for genre in genres:
            genre_per_user = data_file.loc[(data_file['userId'] == id) & (
                data_file['genres'] == genre)]
            mean = genre_per_user["rating"].mean()
            per_user_means[str(genre)] = mean

        mean_file = mean_file.append(per_user_means, ignore_index=True)

    mean_file.to_csv("newmean.csv", index=False)


###################################################################

def create_clusters():

    mean_file = pd.read_csv('newmean.csv').fillna(0)
    ratings_df = pd.read_csv('ratings.csv')
    y = KMeans()
    mean_file['clusters'] = y.fit_predict(mean_file[genres[1:]])
    for id in range(1,user_ids + 1): 
        ratings_df.loc[ratings_df['userId'] == id, 'cluster'] = int(mean_file['clusters'].loc[mean_file['userId'] == id ])

    return ratings_df, mean_file

def unseen_movies(user_id,movie_id,rating_df, mean_df):
    cluster_movies = set()
    user_movies = set()
    user_cluster = mean_df.loc[mean_df['userId'] == user_id , ['clusters']].values[0]
    movies_in_cluster = rating_df.loc[rating_df['cluster'] == float(user_cluster) , ['movieId']]
    movies_per_user = rating_df.loc[rating_df['userId'] == user_id, ['movieId']]
    for idx in movies_in_cluster.index:
        cluster_movies.add(movies_in_cluster['movieId'][idx]) 
    for idx in movies_per_user.index:
        user_movies.add(movies_in_cluster['movieId'][idx]) 
    if movie_id in user_movies:
        return float(rating_df.loc[(rating_df['userId'] == user_id) & (rating_df['movieId'] == movie_id ), ['rating']].values[0])
    elif (movie_id not in user_movies) and (movie_id in cluster_movies):
        return float(rating_df.loc[(rating_df['cluster'] == float(user_cluster)) & (rating_df['movieId'] == movie_id ), ['rating']].mean())
    else: return 0 


#create_mean_file()
#create_clusters()
#fill_movies() 
ratings_df, mean_df = create_clusters()
var = unseen_movies(1,785,rating_df,mean_df)
print(var)

