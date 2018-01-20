import urllib.request
import feedparser

def ScholarlyApifunc(keyPhrase):
    url = 'http://export.arxiv.org/api/query?search_query=all:'+keyPhrase+'&start=0&max_results=1'
    data = urllib.request.urlopen(url).read()
    d = feedparser.parse(data)

    if d.entries != []:
        url = d.entries[0]["id"]
        title = d.entries[0]["title"]
        summary = d.entries[0]["summary"]
        authors = d.entries[0]["authors"][0]["name"]
        published = d.entries[0]["published"]

        if len(d.entries[0]["authors"]) > 1:
            authors += "et al."
    else:
        url = None
        title = None
        summary = None
        authors = None
        published = None
    return (url, title, summary, authors, published)
