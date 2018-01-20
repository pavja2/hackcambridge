#Imports
import time
import requests
import cv2
import operator
import numpy as np

# Variables
#url of Microsoft Vision API
_url = 'https://westus.api.cognitive.microsoft.com/academic/v1.0/interpret'
#Account Key
_key = '40f1a730d26d439fa1b5a8e2a0adb66b'
_maxNumRetries = 10

"""
Helper function to process the request to Microsoft Academic Knowledge Interpreter API

Parameters:
json: Used when processing images from its URL. See API Documentation
data: Used when processing image read from disk. See API Documentation
headers: Used to pass the key information and the data type request
"""
def processRequest(params):
    retries = 0
    result = None

    while True:
        response = requests.request('get', _url, params = params)

        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 200:
            return response.json()
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )
        break


"""
Main function to interpret text words

word = Text word to interpret
"""
def NLPAPI(word):
    params =   {'query' : word,
                'complete' : 1,
                'count' : 2,
                'subscription-key' : _key}

    logprob = []
    result = []
    json = processRequest(params)

    for i in json["interpretations"]:
        logprob.append(i["logprob"])
        result.append(i["rules"][0]["output"]["value"])

    print(logprob)
    print(result)

NLPAPI("interactive network directory")
