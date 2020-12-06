#IMPORTING MODULES.

from elasticsearch import helpers, Elasticsearch
import requests, json

#END SECTION.

#ELASTICSEARCH QUERY FORMAT.
def search_query(): 
    query = {
        "query": {
            "match": {
                'title': str(input())
            }
        }
    } 
    return query

#END SECTION.

#SEARCH FUNCTION.

def search(es, url):
    es.indices.refresh(index="movies") 
    my_query = search_query() #INSERT TITLE.
    results = requests.get(url, data=json.dumps(my_query), headers={'Content-Type': 'application/json'}) #REQUEST FOR THE SEARCH RESULTS.
    search_hits = json.loads(results.text)['hits']['hits'] #KIND OF FILTERING THE DATA FROM THE JSON THAT GET RESPONED.
    print('Relevance Score\t Title')
    for hit in search_hits:
        print(hit['_score'],'\t',hit['_source']['title'] )

#END SECTION.  



