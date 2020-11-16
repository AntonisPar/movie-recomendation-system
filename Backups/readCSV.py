#MODULES.

import csv, os, requests, json, logging, time
from elasticsearch import helpers, Elasticsearch
from csvToJson import make_json
from progress.bar import FillingCirclesBar


#END SECTION.

#VARIABLES

csvFile  = "movies.csv"
jsonFile = "movies.json"
movieId  = 1
jsonDict = {}

#END SECTION.

#CHECK IF THE FILE EXISTS AND IF IS TRUE CONVERT TO JSON AND PUT THE DATA TO A DICTIONARY.
try:
    csvCheck = open(csvFile)
    csvCheck.close()
except IOError:
    print("Please Move The CSV In The Current Directory")
    exit()

try:
    jsonCheck = open(jsonFile)
    jsonCheck.close()
except IOError:
    print("Converting CSV File To JSON")
finally:
    make_json(csvFile,jsonFile)

with open(jsonFile) as jsonData:
    jsonDict = json.load(jsonData) 

#END SECTION.


#IMPORT THE DATA TO ELASTICSEARCH.  

es = Elasticsearch() #CONNECT TO ELASTICSEARCH.
es.indices.create(index='movies', ignore=400) #CREATE THE INDEX.

bar = FillingCirclesBar('Uploading Data', max = len(jsonDict)) #PROGRESS BAR.

for movieId in jsonDict: #IMPORTING DATA.
    res = es.index( index="movies", id=movieId, body=jsonDict[movieId] )
    bar.next() 
bar.finish()

es.indices.refresh(index="movies")

res = es.search(index="movies", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])

#END SECTION.  
