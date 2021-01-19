import re
import operator
import string
import tqdm
import pandas as pd 
import numpy as np 
import tensorflow as tf
import tensorflow.keras as keras
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Activation, Dense, Dot, Embedding, Flatten, GlobalAveragePooling1D, Reshape

movies_csv = pd.read_csv('movies.csv')
rating_csv = pd.read_csv('ratings.csv')
titles = movies_csv['title'].str.replace(r"\(.*\)","")
user_movies = rating_csv[['userId','movieId']]
user_ratings = rating_csv['rating']

combined_df = pd.merge(movies_csv, rating_csv, on='movieId', how='inner')
combined_df = combined_df[['userId','title','genres','rating']]
categories = combined_df['genres'].str.split('|') 
categories_raw = combined_df['genres'].tolist()
categories_raw = set(categories_raw)
print(combined_df.loc[combined_df['title'] == 'toy' ,'genres'])

test = []

for i in combined_df.values:
    user_string = 'user' + str(i[0])
    title = re.sub(r"\(.*\)","",i[1])
    test.append(user_string + " "+ title)



genre = set() 

for category in categories:
    for i in category:
        genre.add(i.lower())


for i in genre:
    genre.remove(i)
    cleared_genre = i.translate(str.maketrans('', '', string.punctuation)) 
    genre.add(cleared_genre)


values = sorted(list(genre))
valuess = np.array(values)


label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(valuess)

onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

genre_dict = dict()

for i in range(0,len(values)):
    genre_dict[values[i]] = list(onehot_encoded[i]) 


onehot_dict = dict()
for i in categories_raw:
    splitted = i.split('|')
    bitwise_or_genre = []
    bitwise_or_genre = np.zeros(len(genre),int)
    for j in  splitted:
        j = j.lower().translate(str.maketrans('','',string.punctuation))
        one_hot_code = genre_dict[j]
        one_hot_code = np.array(one_hot_code,int)
        bitwise_or_genre = np.bitwise_or(bitwise_or_genre,one_hot_code)
    onehot_dict[i] = list(bitwise_or_genre)

from elasticsearch import helpers, Elasticsearch
import pandas as pd
import requests
import json

def custom_search(es, url):

    df = pd.read_csv('ratings.csv')
    es.indices.refresh(index="movies")
    print("Please insert your User ID: ", end = ' ')
    uID = int(input())

    print("Search for a movie: ", end = ' ')
    query = {
        "query": {
            "match": {
                # search against the 'title' field
                'title': str(input())
            }
        }
    }

    response = requests.get(url, data=json.dumps(query), headers={
                            'Content-Type': 'application/json'})
    search_hits = json.loads(response.text)['hits']['hits']
    rating_by_user = df.loc[(df['userId'] == uID)]
    rating_result = {}
    new_score = {}

    for hit in search_hits:
        es_movie_genre = hit['_source']['genres']
        print( onehot_dict[es_movie_genre])
custom_search(Elasticsearch(), 'http://localhost:9200/movies/_doc/_search')

