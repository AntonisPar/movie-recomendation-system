from upload_data import upload_data
from simple_search import search
from custom_search import custom_search
from clusters import *
from elasticsearch import helpers, Elasticsearch

#SOME SIMPLE MENU FUNCTIONS TO MAKE EXECUTION EASIER.

es = Elasticsearch()  # CONNECT TO ELASTICSEARCH.
url = 'http://localhost:9200/movies/_doc/_search'
ratings_with_clusters, mean_with_clusters = create_clusters()


def data_menu():
    print("Would you like to upload the Data to Elasticsearch? [y/N]", end=' ')
    condition = False
    while condition == False:

        option = str(input()).lower()
        if (option == 'y' or option == 'yes'):
            print("Data will be uploaded\n")
            upload_data(es)
            condition = True
        elif (option == 'n' or option == 'no' or option == ""):
            print("Data will not be uploaded")
            condition = True
        else:
            print("Please choose y, n or type nothing for the default option: ", end=' ')


def search_menu():
    print("Search for a movie: ", end=' ')
    search(es, url)

    print("Would you like to search for another movie? [y/N] ", end=' ')
    condition = False
    while condition == False:

        option = str(input()).lower()

        if(option == 'yes' or option == 'y'):
            print("Search for a movie: ", end=' ')
            search(es, url)
            print("Would you like to search for another movie? [y/N]", end=' ')
        elif(option == 'no' or option == 'n' or option == ''):
            condition = True
        else:
            print("Please choose y, n or type nothing for the default option: ", end=' ')


def custom_search_menu():

    custom_search(es, url,ratings_with_clusters,mean_with_clusters)
    print("Would you like to search for another movie? [y/N] ", end=' ')

    condition = False
    while condition == False:
        option = str(input()).lower()

        if(option == 'yes' or option == 'y'):
            custom_search(es, url,ratings_with_clusters,mean_with_clusters)
            print("Would you like to search for another movie? [y/N]", end=' ')
        elif(option == 'no' or option == 'n' or option == ''):
            condition = True
        else:
            print("Please choose y, n or type nothing for the default option: ", end=' ')


def start_menus():
    data_menu()
    condition = True
    while condition == True:
        print("Would you like to use the simple Search or our Custom Search?")
        print("[1] Simple Search")
        print("[2] Custom Search")
        print("[3] Exit")
        print("Write the number that belongs to the search you want to use: ", end = ' ') 
        option = int(input())

        if( option == 1 ):
            search_menu()
            print("would you like to choose another option? [y/N]: ", end = ' ') 
            check = input().lower()
            if (check == 'yes' or check =='y'):
                condition = True 
            elif (check == 'no' or check == 'n' or check == ''):
                condition = False 

        elif( option == 2 ):
            custom_search_menu()
            print("would you like to choose another option? [y/N]: ", end = ' ') 
            check = input().lower()
            if (check == 'yes' or check =='y'):
                condition = True 
            elif (check == 'no' or check == 'n' or check == ''):
                condition = False 
        elif(option == 3): 
            condition = False
start_menus()
