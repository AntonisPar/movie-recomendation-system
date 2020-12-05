from readCSV import uploadData
from search import search

#SOME SIMPLE MENU FUNCTIONS TO MAKE EXECUTION EASIER.

def dataMenu():
    print("Would you like to upload the Data to Elasticsearch? [y/N]", end=' ')
    condition = False
    while condition == False:

        option = str(input()).lower()
        if (option == 'y' or option == 'yes'):
            print("Data will be uploaded\n")
            uploadData()
            condition = True
        elif (option == 'n' or option == 'no' or option == ""):
            print("Data will not be uploaded")
            condition = True
        else:
            print("Please choose y, n or type nothing for the default option: ", end = ' ')


def searchMenu():
    print("Search for a movie: ", end=' ')
    search()

    print("Would you like to search for another movie? [y/N] ", end=' ')
    condition = False
    while condition == False:

        option = str(input()).lower()

        if(option == 'yes' or option == 'y'):
            print("Search for a movie: ", end=' ')
            search()
            print("Would you like to search for another movie? [y/N]", end=' ')
        elif(option == 'no' or option == 'n' or option == ''):
            condition = True
        else:
            print("Please choose y, n or type nothing for the default option: ", end=' ')

dataMenu()
searchMenu()
