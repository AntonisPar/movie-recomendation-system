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


tokenizer = Tokenizer(num_words=len(words))

tokenizer.fit_on_texts(words_list)

dictionary = tokenizer.word_index 

for key,value in dictionary.items():
    dictionary[key]=value+1

def convert_text_to_index_array(text):
  return [dictionary[word] for word in tf.keras.preprocessing.text.text_to_word_sequence(text)]

allWordIndices = []

for text in words_list:
  wordIndices = convert_text_to_index_array(text)
  allWordIndices.append(wordIndices)

final_vectors = []

for i in range(0,len(movies_csv)):
    final_vectors.append(allWordIndices[i])
    genres = categories[i]
    bitwise_or_genre = []
    bitwise_or_genre = np.zeros(len(genre),int)
    if len(genres)>1:
        for j in genres:
            j = j.lower().translate(str.maketrans('','',string.punctuation))
            one_hot_code = genre_dict[j]
            one_hot_code = np.array(one_hot_code,int)
            bitwise_or_genre = np.bitwise_or(bitwise_or_genre,one_hot_code)
        bitwise_or_genre=list(bitwise_or_genre) 
        final_vectors[i].extend(bitwise_or_genre)
        
    else:
        one_hot_code = list(np.array(genre_dict[genres[0].lower().translate(str.maketrans('','',string.punctuation))],int))
        final_vectors[i].extend(one_hot_code)

padded = tf.keras.preprocessing.sequence.pad_sequences(final_vectors,padding='post',truncating='post')
padded_list=padded.tolist() 

movie_dict = dict()

for idx, movie_id in enumerate(movies_csv['movieId'].tolist()):
    movie_dict[movie_id] = padded_list[idx] 

x_ds = []
user_id_dict = dict()
max_token = dictionary[max(dictionary, key=dictionary.get)]

for id in rating_csv[['userId','movieId']].values: 
    temp =[]
    user_id_dict[id[0]] = id[0]+max_token
    temp.append(user_id_dict[id[0]].tolist())
    temp.extend(movie_dict[id[1]])
    x_ds.append(temp)




x_ds = np.asarray(x_ds)
rating_csv['rating'] =  rating_csv['rating'].astype(np.float32)
rating_csv['rating'] = rating_csv['rating'].apply(lambda x: x/5).values
#y = rating_csv[['userId','rating']].values
#y = []
#for id in rating_csv[['rating','movieId']].values:
#    temp =[]
#    temp.append(id[0].tolist())
#    temp.extend(movie_dict[id[1]])
#    y.append(temp)
#
#y=np.asarray(y)

y_df = rating_csv['rating'].values.tolist()

y_ds=[]
for i in y_df:
    temp = [] 
    temp.append(i)
    y_ds.append(temp)


y_ds = np.asarray(y_ds)

train_indices = int(0.9 * rating_csv.shape[0])
x_train, x_val, y_train, y_val = (
    x_ds[:train_indices],
    x_ds[train_indices:],
    y_ds[:train_indices],
    y_ds[train_indices:],
)

print(y_train.shape)
print(x_train.shape)

embedding_dim=35

embedding_dim=35

model = Sequential([
  Embedding(max_token+1, embedding_dim, name="embedding"),
  GlobalAveragePooling1D(),
  Dense(16, activation='relu'),
  Dense(1)
])

model.compile(optimizer='sgd',
              loss='mse',
              metrics=['accuracy'])

model.fit(
    x_train,
    y_train,
    validation_data=(x_val,y_val), 
    epochs=5,
)
