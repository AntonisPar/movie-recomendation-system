import string

import pandas as pd

import gensim

movies_csv = pd.read_csv('movies.csv') 
titles = movies_csv['title'].str.replace(r"\(.*\)","").to_list()



words = set()
kappa=[]

words_list= []
for sentece in titles:
    words=[]
    sen = ''
    words_in_sentence = sentece.split()
    for i in words_in_sentence:
        cleared_word = i.lower().translate(str.maketrans('', '', string.punctuation))
        words.append(cleared_word)

    words_list.append(words)





model = gensim.models.Word2Vec(
        words_list,
        min_count=1,
        iter=10)


vocab = list(model.wv.vocab)
#print(vocab)

print(model.wv.__getitem__('toy'))
