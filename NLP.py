import OCRAPI, NLPAPI, WikipediaAPI

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
print(NLPfun("test.jpg"))
