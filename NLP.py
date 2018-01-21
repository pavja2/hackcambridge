import OCRAPI, NLPAPI, WikipediaAPI, arXivAPI, CrossRefAPI, KnowledgeGraphAPI

def NLPfun(imageName):

    keyphrases = NLPAPI.keyWordExtractorAPI(OCRAPI.OCRAPIfunc(imageName))

    data = [[-1 for i in range(len(keyphrases))] for j in range(5)]

    for k in range(0,len(keyphrases)):

        data[0][k] = KnowledgeGraphAPI.academiaTest(keyphrases[k])

        if data[0][k] == False:
            #title, extract, imurl, url
            (data[1][k],data[2][k],data[3][k],data[4][k]) = WikipediaAPI.WikipediaAPIfunc(keyphrases[k])
        else:
            #url, titles, authors, published
            (data[1][k],data[2][k],data[3][k],data[4][k]) = arXivAPI.arXivAPIfunc(keyphrases[k])
        #url, titles, authors, published
        #(data[2][0][k],data[2][1][k],data[2][2][k],data[2][3][k]) = CrossRefAPI.CrossRefAPIfunc(keyphrases[k])

    i=0
    while i < len(data[0]):
        if data[1][i] == None and data[2][i] == None and data[3][i] == None and data[4][i] == None:
                for k in range(5):
                    del data[k][i]
        else:
            i+= 1

    #print(data)
    return (data)

#Example usage
print(NLPfun("test.jpg"))
