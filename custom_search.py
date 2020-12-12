#from readCSV import uploadData
from elasticsearch import helpers, Elasticsearch
from clusters import  *
import pandas as pd
import requests
import json

def custom_search(es, url,ratings_with_clusters,mean_with_clusters):

    df = pd.read_csv('ratings.csv')
    es.indices.refresh(index="movies")
    print("Please insert your User ID: ", end = ' ')
    user_id = int(input())

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
    new_score = {}

    for hit in search_hits:
        es_movie_id = int(hit['_source']['movieId'])
        rating_by_movie = df.loc[(df['movieId'] == es_movie_id)]
        es_bm_score = float(hit['_score'])
        es_movie_title = hit['_source']['title']

        rating = unseen_movies(user_id,es_movie_id,ratings_with_clusters,mean_with_clusters)
        score_calc = (0.25 * es_bm_score) + (0.5 * rating ) + (
        0.25 * rating_by_movie['rating'].mean())
        new_score[es_movie_title] = score_calc

    sorted_results = sorted(
        new_score.items(), key=lambda x: x[1], reverse=True)

    print('Relevance Score\t Title')
    for i in sorted_results:
        print("%.6f" % i[1], '\t', i[0])


