#MODULES.

import csv
import os
import requests
import json
import logging
import time
import pandas as pd
from elasticsearch import helpers, Elasticsearch
from progress.bar import FillingCirclesBar

#END SECTION.

#IMPORTING SETTINGS FOR ELASTICSEARCH.

#END SECTION.

#VARIABLES

es = Elasticsearch()  # CONNECT TO ELASTICSEARCH.
settings_file = "settings.json"
csv_file = "movies.csv" # SPECIFY THE PATH TO THE CSV FILE.

try: 
    csv_reader = pd.read_csv(csv_file).T.to_dict()
    print(csv_reader)
    with open(settings_file) as settings:
        esSettings = json.load(settings)
except IOError:
    print("Please move the movies.csv or settings.json to the current directory or specify the path to the csv_file or json_file variable accordingly")
    exit()

#END SECTION.

#CHECK IF THE FILE EXISTS AND IF IS TRUE IMPORT THE DATA TO ELASTICSEARCH.

def uploadData():

    es.indices.create(index='moviestest', ignore=400, body=esSettings) # CREATE THE INDEX.
    for (key, docs_data) in csv_reader.items():
        res = es.index(index="moviestest", id=key , body=docs_data)
    print("Data uploaded successfully") 

#END SECTION.
uploadData()
