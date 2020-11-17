#from readCSV import uploadData
from elasticsearch import helpers, Elasticsearch
import requests
import json

es = Elasticsearch() #CONNECT TO ELASTICSEARCH.
es.indices.refresh(index="movies") 
myQuery = str(input())

query = {
    'query': {
        'match': {
            # search against the 'title' field
            'query': myQuery
        }
    }
}
print(es.search(index='movies',body=query ,size=1000))


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
