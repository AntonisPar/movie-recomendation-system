import re
import operator
import string
import pandas as pd 
import numpy as np 
import tensorflow as tf
import tensorflow.keras as keras
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Activation, Dense, Dot, Embedding, Flatten, GlobalAveragePooling1D, Reshape

from wembedding2 import predict_rating,create_model

tokens, onehot = create_model()

print(predict_rating(7, 'Toy Story (123)', 'Adventure|Animation|Children|Comedy|Fantasy',tokens,onehot))


