#MODULES.

import csv, os, requests, json, logging, time
from elasticsearch import helpers, Elasticsearch
from progress.bar import FillingCirclesBar 

#END SECTION.

#IMPORTING SETTINGS FOR ELASTICSEARCH.

with open("settings.json") as settings:
    esSettings = json.load(settings)

#END SECTION.

#VARIABLES

csvFile  = "movies.csv" #SPECIFY THE PATH TO THE CSV FILE.
es = Elasticsearch() #CONNECT TO ELASTICSEARCH.
es.indices.create(index='movies', ignore=400, body=esSettings) #CREATE THE INDEX.  

#END SECTION.  

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
