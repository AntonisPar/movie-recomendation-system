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

def uploadData():
    try:
        with open(csvFile, encoding='utf-8') as csv_data: 
            csv_reader = csv.DictReader(csv_data) 
            for docsData in csv_reader: 
                lineNum = csv_reader.line_num - 1
                res = es.index( index="movies", id=lineNum, body=docsData )
        print("Data uploaded successfully")
    except IOError: 
        print("Please Move The CSV To The Current Directory Or Specify The Path To The csvFile Variable")
        exit() 

#END SECTION.  
