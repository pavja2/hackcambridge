
import requests
import json

def WikipediaAPI(keyphrase):


############################ ACCESS TITLE AND EXTRACT ############################
    params = {
        "action" : "query",
        "prop" : "extracts",
        "exchars" : 200,
        "exlimit" : 1,
        "explaintext" : "",
        "format" : "json",
        "titles" : keyphrase
    }

    while True:
        response = requests.get("https://en.wikipedia.org/w/api.php",params)
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

            #get title and extract (will only loop once)
            for key in result["query"]["pages"]:
                title = result["query"]["pages"][key]["title"]
                extract = result["query"]["pages"][key]["extract"]
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break

############################ ACCESS MAIN ARTICLE IMAGE FILE NAME ############################

    params = {
        "action" : "query",
        "prop" : "pageimages",
        "format" : "json",
        "titles" : keyphrase,
        "piprop" : "thumbnail",
        "pithumbsize" : "200"
    }

    while True:
        response = requests.get("https://en.wikipedia.org/w/api.php",params)
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

            #get article image filename
            for key in result["query"]["pages"]:
                filename = result["query"]["pages"][key]["thumbnail"]["source"]
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break


#Example Function Run
# WikipediaAPI("Elon Musk")
