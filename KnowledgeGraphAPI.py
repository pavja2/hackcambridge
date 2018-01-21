"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib.parse
import urllib.request

def academiaTest(keyword):
    api_key =  "AIzaSyCBC2m9paG7ROZJGh_LTwZj8g6CW8WGAls"
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': keyword,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read())

    if len(response["itemListElement"]) > 0 and float(response["itemListElement"][0]["resultScore"]) > 300.0:
        types = response["itemListElement"][0]["result"]["@type"]

        if "Person" in types:
            desc = response["itemListElement"][0]["result"]["description"]
            for word in ["math","stat","physicist","professor","scientist","lecturer","author","novelist","biologist","chemist","geogra","astronomer","historian","theoretical","linguist","lawyer","doctor","researcher","philosoph","naturalist"]:
                if word in desc.lower():
                    return True

    return False

#Example Use
#print(academiaTest("Marie Curie"))
