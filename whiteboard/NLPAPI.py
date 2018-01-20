#Imports
import time
import requests

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


def keyWordExtractor(text):
    from rake_nltk import Rake

    r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

    # If you want to provide your own set of stop words and punctuations to
    # r = Rake(<list of stopwords>, <string of puntuations to ignore>)

    r.extract_keywords_from_text(text)

    print(r.get_ranked_phrases()) # To get keyword phrases ranked highest to lowest.
"""

def keyWordExtractorAPI(text):
    import http.client, urllib, base64
    import json

    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '3ca4fd37d935431ba6a1c8bf28eef522',
    }

    params = urllib.parse.urlencode({
    })

    body = {
            "documents": [
                {
                    "language": "en",
                    "id": "1",
                    "text": text
                }
            ]
        }

    try:
        print(text)
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        print(data)
        keyphrases = []
        for k in data["documents"][0]["keyPhrases"]:
            keyphrases.append(k)
        conn.close()
        return keyphrases
    except Exception as e:
        print(e)

#Example Use
#print(keyWordExtractorAPI("It is expected that you will be familiar with most of the following I The notion polynomial time, space, etc. I Big O notation I Basic probability theory - expectation, independence, etc. It’d be helpful if (though not necessary that) you’ve seen at least some of the following I Basic complexity theory such as NP-completeness I Applied Machine Learning I Optimisation algorithms - Linear Programming"))
