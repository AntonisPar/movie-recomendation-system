#from readCSV import uploadData
from elasticsearch import helpers, Elasticsearch
import requests
import json

es = Elasticsearch() #CONNECT TO ELASTICSEARCH.
es.indices.refresh(index="movies") 

query = {
    'query': {
        'match_all': {
            # search against the 'title' field
            
        }
    }
}

def search(query, headers):
    url = 'http://localhost:9200/movies/_doc/_search'
    response = requests.get(url, data=json.dumps(query), headers=headers)
    
    # the response contains other information, such as time it took to
    # give the response back, here we are only interested in the matched
    # results, which are stored under 'hits'
    search_hits = json.loads(response.text)['hits']['hits']

    print('Num\tRelevance Score\tTitle')
    for idx, hit in enumerate(search_hits):
        print('%s\t%s\t%s' % (idx + 1, hit['_score'], hit['_source']['title']))

search(query, headers={'Content-Type': 'application/json'})

#print("Would you like to upload the Data to Elasticsearch? [y/N]")
#
#check = str(input())
#
#flag = False
#
#while flag==False : 
#
#    if (check == 'y' or check == 'Y' ):
#        print("Data will be uploaded\n")
#        uploadData(es)
#        flag=True
#    elif ( check == 'n' or check=='N' or check == "" ):
#        print("Data will not be uploaded") 
#        flag = True
#    else : print("Please write y or N to choose")
