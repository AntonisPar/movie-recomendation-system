#MODULES.

import csv, os, requests, json, logging, time
from elasticsearch import helpers, Elasticsearch
from progress.bar import FillingCirclesBar 

#END SECTION.

#VARIABLES

csvFile  = "movies.csv" #SPECIFY THE PATH TO THE CSV FILE.
es = Elasticsearch()

#END SECTION.  

settings={
    'settings': {
        'index': {
            'number_of_shards': 1,
            'number_of_replicas': 1,

            # configure our default similarity algorithm explicitly to use bm25,
            # this allows it to use it for all the fields
            'similarity': {
                'default': {
                    'type': 'BM25'
                }
            }
        }
    }
}
es.indices.create(index='movies', ignore=400, body=settings) #CREATE THE INDEX.  
#CHECK IF THE FILE EXISTS AND IF IS TRUE IMPORT THE DATA TO ELASTICSEARCH.

def uploadData(es):
    try:
        with open(csvFile, encoding='utf-8') as csvData: 
            csvReader = csv.DictReader(csvData) 
            for docsData in csvReader: 
                lineNum = csvReader.line_num - 1
                res = es.index( index="movies", id=lineNum, body=docsData ) 
    except IOError: 
        print("Please Move The CSV To The Current Directory Or Specify The Path To The csvFile Variable")
        exit() 

uploadData(es)

#END SECTION.  
