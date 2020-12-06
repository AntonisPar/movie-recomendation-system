#from readCSV import uploadData
from elasticsearch import helpers, Elasticsearch
import pandas as pd
import requests
import json

es = Elasticsearch()  # CONNECT TO ELASTICSEARCH.
es.indices.refresh(index="movies")
url = 'http://localhost:9200/movies/_doc/_search'
df = pd.read_csv('ratings.csv')


def custom_search():

    print("Please insert your User ID: ")
    uID = int(input())

    print("Search for a movie: ")
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

    for idx in rating_by_user.index: # GETTING IMPORT DATA FROM THE DATAFRAME BASED ON THE USER'S INPUT.
        movie_id = int(rating_by_user['movieId'][idx])
        movie_rating = float(rating_by_user['rating'][idx])
        rating_result[movie_id] = movie_rating

    for hit in search_hits: # GETTING THE IMPORT DATA FROM THE GET RESPONSE.
        es_movie_id = int(hit['_source']['movieId'])
        rating_by_movie = df.loc[(df['movieId'] == es_movie_id)]
        es_bm_score = float(hit['_score'])
        es_movie_title = hit['_source']['title']

        if es_movie_id in rating_result: # THE CASE THAT USER RATING FOR THE MOVIE EXISTS.
            score_calc = (0.25 * es_bm_score) + (0.5 * rating_result[es_movie_id]) + (
                0.25 * rating_by_movie['rating'].mean())
            new_score[es_movie_title] = score_calc

        else: # THE CASE THAT USER HAS NOT RATED THE MOVIE.
            score_calc = (0.25 * es_bm_score) + \
                (0.25 * rating_by_movie['rating'].mean())
            new_score[hit['_source']['title']] = score_calc

    sorted_results = sorted(
        new_score.items(), key=lambda x: x[1], reverse=True)

    print('Relevance Score\t Title')
    for i in sorted_results:
        print("%.6f" % i[1], '\t', i[0]) 
custom_search()
