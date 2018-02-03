import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='43f96ab3-69a5-4d92-8bff-3c471730fe45',
  password='yzKNcnEDXFmB',
  version='2017-02-27')

def main():
    aList = [["https://www.cnn.com/2018/02/02/politics/james-comey-nunes-memo/index.html",'date','cnn','Trump',0.0,[]]
             ,["https://www.cnn.com/2018/02/02/politics/rod-rosenstein-donald-trump/index.html",'date','cnn','Trump',0.0,[]]
             ,["https://www.cnn.com/2018/01/30/politics/melania-trump-state-of-the-union-2018/index.html",'date','cnn','Trump',0.0,[]]
             ,["http://www.foxnews.com/politics/2018/02/02/house-memo-states-disputed-dossier-was-key-to-fbi-s-fisa-warrant-to-surveil-members-team-trump.html",'date','fox','Trump',0.0,[]]
             ,["http://www.foxnews.com/politics/2018/02/03/nunes-fisa-memo-sparks-reactions-from-politicians.html",'date','fox','Trump',0.0,[]]
             ,["http://www.foxnews.com/opinion/2018/02/03/gop-memo-raises-serious-questions-about-fbi-and-justice-department-officials-that-demand-answers.html",'date','fox','Trump',0.0,[]]
             ]
    test = analyzeIn(aList)
    print(test)
    print(cnnVsFoxSentiment(test))

   
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
    foxArt =[ x[4] for x in formattedURLS if x[2] == 'fox']
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
    
