import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='43f96ab3-69a5-4d92-8bff-3c471730fe45',
  password='yzKNcnEDXFmB',
  version='2017-02-27')

def main():
   test=[["https://www.cnn.com/2018/02/03/politics/donald-trump-memo/index.html","date","cnn",0,[]],
     ["https://www.cnn.com/2018/02/02/politics/john-mccain-nunes-memo/index.html","date","cnn",0,[]],
     ["https://www.cnn.com/2018/02/03/africa/north-korea-mozambique-sanctions-intl/index.html","date","cnn",0,[]],
     ["https://www.cnn.com/2018/02/03/entertainment/lady-gaga-cancels-tour/index.html","date","cnn",0,[]],
     ["https://www.cnn.com/2018/02/02/sport/super-bowl-lii-preview-eagles-patriots/index.html","date","cnn",0,[]]]
   test2 = analyzeIn(test)
   print(test2)

'''
    Updates the given data of urls with sentiment scores and keywords
:param:A list of lists (String: url,TimeStamp: date,String: networkname,Float: score,[String]:keywords)

'''
def analyzeIn(absUrls):
    for absTuple in absUrls:
        absUrl = absTuple[0]
        absTuple[3] = analyzeSentiment(absUrl)
        absTuple[4] = analyzeKeyWords(absUrl)
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
def analyzeSentiment(absUrl):
    response = natural_language_understanding.analyze(
    url=absUrl,
    features=Features(
        sentiment=SentimentOptions()))
    return float(response['sentiment']['document']['score'])
 

main()
    
