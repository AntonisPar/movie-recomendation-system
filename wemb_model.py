import re
import operator
import string
import os
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Activation, Dense, Dot, Embedding, Flatten, GlobalAveragePooling1D, Reshape

def convert_text(text,words_to_token_dict):
    return [words_to_token_dict[word] for word in tf.keras.preprocessing.text.text_to_word_sequence(text)]

def create_model():

    movies_csv = pd.read_csv('movies.csv')
    rating_csv = pd.read_csv('ratings.csv')
    
    combined_df = pd.merge(movies_csv, rating_csv, on='movieId', how='inner')
    combined_df = combined_df[['userId', 'title', 'genres', 'rating']]
    categories = combined_df['genres'].str.split('|')
    categories_raw = set(combined_df['genres'].tolist())
    
    user_and_movies = []
    
    for i in combined_df.values:
        user_string = 'user' + str(i[0])
        title = re.sub(r"\(.*\)", "", i[1])
        user_and_movies.append(user_string + " " + title)
    
    
    all_genre = set()
    
    for category in categories:
        for i in category:
         cleared_genre = i.translate(str.maketrans(
             '', '', string.punctuation)).lower()
         all_genre.add(cleared_genre)
    
    
    all_genre = np.array(sorted(list(all_genre)))
    
    
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(all_genre)
    
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    
    genre_dict = dict()
    
    for i in range(0, len(all_genre)):
        genre_dict[all_genre[i]] = list(onehot_encoded[i])
    
    onehot_dict = dict()
    
    for i in categories_raw:
    
        splitted = i.split('|')
        bitwise_or_genre = []
        bitwise_or_genre = np.zeros(len(all_genre), int)
        for j in splitted:
            j = j.lower().translate(str.maketrans('', '', string.punctuation))
            one_hot_code = genre_dict[j]
            one_hot_code = np.array(one_hot_code, int)
            bitwise_or_genre = np.bitwise_or(bitwise_or_genre, one_hot_code)
        onehot_dict[i] = list(bitwise_or_genre)
    
    
    words_list = [] 
    words = set()
    
    for sentece in user_and_movies:
        sen = ''
        words_in_sentence = sentece.split()
        for i in words_in_sentence:
            if(len(i) > 1):
                cleared_word = i.lower().translate(str.maketrans('', '', string.punctuation))
                words.add(cleared_word)
                sen = sen + ' ' + cleared_word
    
        words_list.append(sen)
    
    words = list(words)
    
    tokenizer = Tokenizer(num_words=len(words))
    
    tokenizer.fit_on_texts(words_list)
    
    
    words_to_token_dict = tokenizer.word_index
    
    for key, value in words_to_token_dict.items():
        words_to_token_dict[key] = value+1 
    
    if not os.path.exists('model_folder'):
        print('Building Model. Please wait...')
        title_vectors = []
        
        for word in words_list:
          word_token = convert_text(word,words_to_token_dict)
          title_vectors.append(word_token)
        
        final_vectors = []
        
        for i in range(0, len(combined_df)):
            final_vectors.append(title_vectors[i])
            genres = categories[i]
            bitwise_or_genre = []
            bitwise_or_genre = np.zeros(len(all_genre), int)
            if len(genres) > 1:
                for j in genres:
                    j = j.lower().translate(str.maketrans('', '', string.punctuation))
                    one_hot_code = genre_dict[j]
                    one_hot_code = np.array(one_hot_code, int)
                    bitwise_or_genre = np.bitwise_or(bitwise_or_genre, one_hot_code)
                bitwise_or_genre = list(bitwise_or_genre)
                final_vectors[i].extend(bitwise_or_genre)
            else:
                one_hot_code = list(np.array(genre_dict[genres[0].lower().translate(
                    str.maketrans('', '', string.punctuation))], int))
                final_vectors[i].extend(one_hot_code)
        
        
        x_dataset = tf.keras.preprocessing.sequence.pad_sequences(
            final_vectors, padding='post')
        
        max_token = words_to_token_dict[max(
            words_to_token_dict, key=words_to_token_dict.get)]
        
        x_dataset = np.asarray(x_dataset)
        
        combined_df['rating'] = combined_df['rating'].astype(np.float32)
        combined_df['rating'] = combined_df['rating'].apply(
            lambda x: x/5).values  # setting ratings from 0 to 1
        
        y_dataset = combined_df['rating'].values
        
        train_indices = int(0.9 * rating_csv.shape[0])
        x_train, x_val, y_train, y_val = (
            x_dataset[:train_indices],
            x_dataset[train_indices:],
            y_dataset[:train_indices],
            y_dataset[train_indices:],
        )
        
        embedding_dim = 35
        
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
            batch_size=256,
            validation_data=(x_val, y_val),
            epochs=5,
            verbose=1
        )
        
        model.save('model_folder') 
        return words_to_token_dict, onehot_dict, model
    else:
        model = keras.models.load_model("model_folder")
        return words_to_token_dict, onehot_dict, model



def predict_rating(userid, movie_title, genre, words_to_token_dict,onehot_dict,model):

    #model = keras.models.load_model("model_folder")
    modified = []
    user_string = 'user' + str(userid)
    title = re.sub(r"\(.*\)", "", movie_title)
    user_token = words_to_token_dict[user_string]
    modified.append(user_token)
    title = title.translate(str.maketrans(
        "", "", string.punctuation)).lower().split()
    for i in title:
        modified.append(words_to_token_dict[i])
    genre_code = onehot_dict[genre]
    modified.extend(genre_code)
    temp = []
    temp.append(modified)
    padded = tf.keras.preprocessing.sequence.pad_sequences(
        temp, padding='post', maxlen=35)
    result = model.predict(padded) 

    return result[0][0] * 5


#predicted_rating = predict_rating(
#    7, 'Toy Story (123)', 'Adventure|Animation|Children|Comedy|Fantasy')
#print(predicted_rating)
