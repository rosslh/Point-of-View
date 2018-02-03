import json
import tldextract
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='43f96ab3-69a5-4d92-8bff-3c471730fe45',
  password='yzKNcnEDXFmB',
  version='2017-02-27')

def main():
    articles = open("articles.txt","r")
    artList = [line.split() for line in articles.readlines()]
    dates = open("dates.txt","r")
    dateList = [line.split() for line in dates.readlines()]
    urlData = createCSV(artList,dateList)
    print(urlData)
    test = analyzeIn(urlData)
    for i in test:
        print(i)
    
 
#A list of lists [String: url,TimeStamp: date,String: networkname,String: Target, Float: score,[String]:keywords]

articlesLocation = "/Users/student/Documents/Github/QHacks/articles.txt"
datesLocation = "/Users/student/Documents/Github/QHacks/dates.txt"
networkList = []


with open(articlesLocation) as f:
    articleContent = f.readlines()
articleContent = [x.strip() for x in articleContent]

with open(datesLocation) as f:
    dateContent = f.readlines()
dateContent = [x.strip() for x in dateContent]

for articleURL in articleContent:
    if articleURL.find("cnn") == -1:
        networkList.append("fox")
    else:
        networkList.append("cnn")

finalList = []

print(articleContent)
print(dateContent)
print(networkList)

for i in range(len(articleContent)-1):
    tempList = [];
    tempList.append(articleContent[i])
    tempList.append(dateContent[i])
    tempList.append(networkList[i])
    tempList.append(None)
    tempList.append(None)
    finalList.append(tempList)

print(finalList)
'''
    Updates the given data of urls with sentiment scores and keywords
:param:A list of lists [String: url,TimeStamp: date,String: networkname,String: Target, Float: score,[String]:keywords]

'''
def analyzeIn(absUrls):
    for absTuple in absUrls:
        absUrl = absTuple[0]
        absTuple[4] = analyzeSentiment(absUrl,absTuple[3])
        absTuple[5] = analyzeKeyWords(absUrl)
    return absUrls


"""
    Analyzes content for major keywords.
:param absUrl: Article Url
:returns: list of strings
"""
def analyzeKeyWords(absUrl):
    response = natural_language_understanding.analyze(
        url=absUrl,
        features=Features(
            keywords=KeywordsOptions(
                limit=3)))
    keywords = [i['text'] for i in response['keywords']]
    return keywords
    
"""
    Analyzes content for general sentiment/tone
:param absUrl: Article Url
:returns: floating point value between -1 and 1. -1 being most negative and
          1 being most positive.
"""
def analyzeSentiment(absUrl,target):
    response = natural_language_understanding.analyze(
        url=absUrl,
        features=Features(
            sentiment=SentimentOptions(
              targets=[target])))
    return response['sentiment']['targets'][0]['score']
    
 

def cnnVsFoxSentiment(formattedURLS):
    cnnArt = [ x[4] for x in formattedURLS if x[2] == 'cnn'] 
    foxArt =[ x[4] for x in formattedURLS if x[2] == 'foxnews']
    cnnAvg = 0
    foxAvg = 0
    try:
        cnnAvg = (sum(cnnArt))/(len(cnnArt))
    except:
        pass
    try:
        foxAvg = (sum(foxArt))/(len(foxArt))
    except:
        pass
    return [cnnAvg,foxAvg]

main()
    
