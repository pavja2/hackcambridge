<<<<<<< HEAD:NLP.py
import OCRAPI, NLPAPI, WikipediaAPI

def NLPfun(imageName):

    keyphrases = NLPAPI.keyWordExtractorAPI(OCRAPI.OCRAPIfunc(imageName))

    titles = [-1]*len(keyphrases)
    extracts = [-1]*len(keyphrases)
    images = [-1]*len(keyphrases)
    url = [-1]*len(keyphrases)

    for k in range(0,len(keyphrases)):
        (titles[k],extracts[k],images[k], url[k]) = WikipediaAPI.WikipediaAPIfunc(keyphrases[k])

    i=0

    while i < len(titles):
        if titles[i] == None:
            del titles[i]
            del extracts[i]
            del images[i]
            del url[i]
        else:
            i+= 1

    return (titles, extracts, images, url)

#Example usage
print(NLPfun("test.jpg"))
=======
from whiteboard import OCRAPI, NLPAPI, WikipediaAPI

def NLPfun(imageName):

    keyphrases = NLPAPI.keyWordExtractorAPI(OCRAPI.OCRAPIfunc(imageName))

    titles = [-1]*len(keyphrases)
    extracts = [-1]*len(keyphrases)
    images = [-1]*len(keyphrases)

    for k in range(0,len(keyphrases)):
        (titles[k],extracts[k],images[k]) = WikipediaAPI.WikipediaAPIfunc(keyphrases[k])

    i=0

    while i < len(titles):
        if titles[i] == None:
            del titles[i]
            del extracts[i]
            del images[i]
        else:
            i+= 1

    return (titles, extracts, images)

#Example usage
#print(NLPfun("test.jpg"))
>>>>>>> 50a0e20fe612a7adbead3b7b160cba53fa4905af:whiteboard/NLP.py
