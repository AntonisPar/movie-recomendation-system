import re
import string
import tqdm
import pandas as pd 
import numpy as np 
import tensorflow as tf
from tensorflow import keras 
from keras import layers
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Activation, Dense, Dot, Embedding, Flatten, GlobalAveragePooling1D, Reshape

movies_csv = pd.read_csv('movies.csv') 
rating_csv = pd.read_csv('ratings.csv')
titles = movies_csv['title'].str.replace(r"\(.*\)","").to_list() 
categories = movies_csv['genres'].str.split('|') 
user_movies = rating_csv.loc[rating_csv['userId'] == 1, ['movieId']]
user_ratings = rating_csv.loc[rating_csv['userId'] == 1, ['rating']]
user_movies = user_movies['movieId'].values.tolist()


genre = set() 

for category in categories:
    for i in category:
        genre.add(i.lower())


for i in genre:
    genre.remove(i)
    cleared_genre = i.translate(str.maketrans('', '', string.punctuation)) 
    genre.add(cleared_genre)

words_list= [] 
words = set()
for sentece in titles:
    sen = ''
    words_in_sentence = sentece.split()
    for i in words_in_sentence:
        cleared_word = i.lower().translate(str.maketrans('', '', string.punctuation))
        words.add(cleared_word)
        sen = sen + ' ' + cleared_word

    words_list.append(sen)

words = list(words)


vectorize_layer = TextVectorization(
 max_tokens=len(words)+1,
 output_mode='int',
 output_sequence_length=32
 )


vectorize_layer.adapt(words_list)

model = tf.keras.models.Sequential()

model.add(tf.keras.Input(shape=(1,), dtype=tf.string))

model.add(vectorize_layer)


input_data = [["toy "], ["the gay"]]


print(model.predict(input_data))
#print(vectorize_layer.get_vocabulary())
