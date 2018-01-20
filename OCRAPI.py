#Imports
import time
import requests
import cv2
import operator
import numpy as np

# Variables
#url of Microsoft Vision API
_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'
#Account Key
_key = '09aadc1e91174ff1b8d150f1a52b799c'
_maxNumRetries = 10

"""
Helper function to process the request to Project Oxford (Microsoft Vision API)

Parameters:
json: Used when processing images from its URL. See API Documentation
data: Used when processing image read from disk. See API Documentation
headers: Used to pass the key information and the data type request
"""
def processRequest( json, data, headers, params ):
    retries = 0
    result = None

    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 202:
            result = response.headers['Operation-Location']
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )
        break

    return result

"""
Helper function to get text result from operation location

Parameters:
operationLocation: operationLocation to get text result, See API Documentation
headers: Used to pass the key information
"""
def getOCRTextResult( operationLocation, headers ):
    retries = 0
    result = None

    while True:
        response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
        if response.status_code == 429:
            print("Message: %s" % (response.json()))
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break
        elif response.status_code == 200:
            result = response.json()
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break
    return result

"""
Main function to pass image stored in file path to Microsoft Vision API

file_path = Path to JPEG image file on server
"""
def OCRAPI(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        data = f.read()

    # Computer Vision parameters
    params = {'handwriting' : 'true'}

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None

    operationLocation = processRequest(json, data, headers, params)

    result = None
    if (operationLocation != None):
        headers = {}
        headers['Ocp-Apim-Subscription-Key'] = _key
        while True:
            time.sleep(1)
            result = getOCRTextResult(operationLocation, headers)
            if result['status'] == 'Succeeded' or result['status'] == 'Failed':
                break

    # Load the original image, fetched from the URL
    if result is not None and result['status'] == 'Succeeded':
        lines = result['recognitionResult']['lines']
        for i in range(len(lines)):
            words = lines[i]['words']
            for j in range(len(words)):
                text += words[j]['text'] + ' '
            text = text[:-1] + '\n'
    return text
