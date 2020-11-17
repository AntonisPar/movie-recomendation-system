#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# use sys for system arguments passed to script
import sys, json

# import the Elasticsearch client library
from elasticsearch import Elasticsearch

# create a client instance of Elasticsearch
client = Elasticsearch("http://localhost:9200")

try:
    INDEX_NAME = sys.argv[1]
except IndexError as err:
    print ("IndexError - Script needs the Elasticsearch index name:", err)
    quit()

def make_query(filter):
    index_exists = client.indices.exists(index=INDEX_NAME)

    # check if the index exists
    if index_exists == True:
        print ("INDEX_NAME:", INDEX_NAME, "exists.")
        print ("FILTER:", filter, "\n")

        try:

            # pass filter query to the client's search() method
            response = client.search(index=INDEX_NAME, body=filter,size=1000)
            #print(response)

            # print the query response
            print ('response["hits"]:', len(response["hits"]))
            print ('response TYPE:', type(response))

            # iterate the response hits
            print ("\nDocument %d hits:" % response['hits']['total']['value'])
            for hit in response['hits']['hits']:
                print(hit["_source"])
        except Exception as err:
            print ("search(index) ERROR", err)
            response = {"error": err}
    # return an empty dict if index doesn't exist
    else:
        response = {}

    return response


def main():

    # declare variable for system arguments list
    sys_args = sys.argv

    # remove Python script name from args list
    sys_args.pop(0)

    # quit the script if there are not exactly 3 arguments
    if len(sys_args) != 2:
        print ("Three arguments needed. You provided:", sys_args)
        print ("First argument is index, and next two are the field and query:", sys_args)
        quit()

    else:

        field_name = "title"
        value = sys_args[1]

        # pass the field name and value args to filter dict
        filter = {
            'query': {
                'match': {
                    field_name : value
                }
            }
        }

    # pass the filter dict to the make_query() function
    resp = make_query(filter)

# have interpreter call the main() func
if __name__ == "__main__":
    main()