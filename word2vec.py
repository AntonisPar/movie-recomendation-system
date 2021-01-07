import pandas as pd 
import tensorflow as tf
import string
import re
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Activation, Dense, Dot, Embedding, Flatten, GlobalAveragePooling1D, Reshape
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

movies_csv = pd.read_csv('movies.csv') 
titles = movies_csv['title'].str.replace(r"\(.*\)","")

print(titles)


def clear_sentences(data):
    lowercase = tf.strings.lower(data)
    return tf.strings.regex_replace(lowercase,
            '[%s]' % re.escape(string.punctuation), '')

vocab_size = 4069
seq_len = 20

vectorize_layer = TextVectorization(
    standardize=clear_sentences(titles.values),
    max_tokens=vocab_size,
    output_mode='float',
    output_sequence_length=seq_len)

vectorize_layer.adapt(text_ds.batch(1024)) 
inverse_vocab = vectorize_layer.get_vocabulary()
print(inverse_vocab)

def vectorize_text(text):
  text = tf.expand_dims(text, -1)
  return tf.squeeze(vectorize_layer(text))

# Vectorize the data in text_ds.
text_vector_ds = text_ds.batch(1024).prefetch(AUTOTUNE).map(vectorize_layer).unbatch()


#import pandas as pd 
###import tensorflow as tf
##from tensorflow.keras.preprocessing.text import one_hot
#import nltk
#import gensim
#
##
#df_clean = pd.DataFrame({'clean': titles})
#sent = [row.split(',') for row in df_clean['clean']]
#
##print(sent)
#
#
#model = gensim.models.Word2Vec(
#        sent,
#        size=100,
#        window=5,
#        min_count=1,
#        workers=10,
#        sg = 1,
#        iter=10)
#
#
#w1 = 'Postman'
#print(model.wv.most_similar (positive=w1))
#
#
#
#
##model = gensim.models.Word2Vec(titles.to_list(), size = 1000)
#vocab = list(model.wv.vocab)
##
##print(vocab)
##
##
##target = titles.pop()
##print ( target )
##
##dataset = tf.data.Dataset.from_tensor_slices( titles.values )
##
##for feat in dataset.take(5):
##    print(feat)
