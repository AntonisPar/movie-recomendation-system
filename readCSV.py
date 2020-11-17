#MODULES.

import csv, os, requests, json, logging, time
from elasticsearch import helpers, Elasticsearch
from progress.bar import FillingCirclesBar 

#END SECTION.

#VARIABLES

csvFile  = "movies.csv" #SPECIFY THE PATH TO THE CSV FILE.
es = Elasticsearch() #CONNECT TO ELASTICSEARCH.
es.indices.create(index='movies', ignore=400) #CREATE THE INDEX.

#END SECTION.  

#CHECK IF THE FILE EXISTS AND IF IS TRUE IMPORT THE DATA TO ELASTICSEARCH.

try:
    with open(csvFile, encoding='utf-8') as csvData: 
        csvReader = csv.DictReader(csvData) 
        for docsData in csvReader: 
            lineNum = csvReader.line_num - 1
            res = es.index( index="movies", id=lineNum, body=docsData )
    es.indices.refresh(index="movies") 

except IOError: 
    print("Please Move The CSV To The Current Directory Or Specify The Path To The csvFile Variable")
    exit() 

#END SECTION.  

#res = es.search(index="movies", body={"query": {"match_all": {}}})
#print("Got %d Hits:" % res['hits']['total']['value'])
#for hit in res['hits']['hits']:
#    print("%(movieId)s %(title)s: %(genres)s" % hit["_source"])
