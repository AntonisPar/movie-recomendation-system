#MODULES.

import os
import json
import pandas as pd
from elasticsearch import helpers, Elasticsearch
from progress.bar import FillingCirclesBar

#END SECTION.


#VARIABLES

settings_file = "settings.json" #SPECIFY THE PATH TO SETTINGS FILE.
csv_file = "movies.csv" # SPECIFY THE PATH TO THE CSV FILE.

#CHECKING IF FILE EXISTS.

if os.path.isfile(settings_file):
    with open(settings_file) as settings:
        es_settings = json.load(settings) #IMPORT SETTINGS FOR ELASTICSEARCH.
else:
    print("Please move the settings.json to the current directory or specify the path to json_file here: ", end= ' ')
    settings_file=input()

#END SECTION.

#IMPORT THE DATA TO ELASTICSEARCH.

def upload_data(es): 
    for csv_df in pd.read_csv(csv_file, index_col=False, chunksize=500000): #MEMORY MANAGMENT JUST IN CASE.
        csv_reader = csv_df.T.to_dict() #TRANSFORM CSV TO DICT CAUSE IT HAS SIMILAR STRUCTURE AS JSON FILE.
        with FillingCirclesBar("Uploading Data: ", max = len(csv_df)) as bar:
            es.indices.create(index='movies', ignore=400, body=es_settings) # CREATE THE INDEX.
            for (key, docs_data) in csv_reader.items():
                res = es.index(index="movies", id=key+1, body=docs_data)
                bar.next()
    print("Data uploaded successfully") 

#END SECTION.
