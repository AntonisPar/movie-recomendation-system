#from readCSV import uploadData
from elasticsearch import helpers, Elasticsearch
import requests
import json

es = Elasticsearch() #CONNECT TO ELASTICSEARCH.
es.indices.refresh(index="movies") 
url = 'http://localhost:9200/movies/_doc/_search'

query = {
    "query": {
        "match": {
            # search against the 'title' field
            'title': str(input())
        }
    }
} 

def search(myQuery):
    res = requests.get(url, data=json.dumps(query), headers={'Content-Type': 'application/json'}) 
    search_hits = json.loads(res.text)['hits']['hits']
    print('Relevance Score\t Title')
    for hit in search_hits:
        print(hit['_score'],'\t',hit['_source']['title'] )

search(query)

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
