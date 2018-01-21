from habanero import Crossref
import urllib.request
import feedparser

def CrossRefAPIfunc(keyPhrase):
    cr = Crossref()
    x = cr.works(query = keyPhrase)

    if x["message"]["total-results"] > 0:
        x = x['message']["items"][0]
        date = x["indexed"]["date-parts"][0]
        #referenceCount = x["is-referenced-by-count"]
        title = x["title"][0]

        if "author" in x:
            authors = x["author"][0]["given"] + x["author"][0]["family"]
            if len(x["author"]) > 1:
                authors += " et al."
        else:
            authors = None
        url = x["URL"]
        #score = x["score"]
    else:
        date = None
        #referenceCount = None
        title = None
        author = None
        url = None
        #score = -1
    return (url, title, authors, date)
#Example Usage
#print(CrossRefAPIfunc("Deep Learning"))
