import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='43f96ab3-69a5-4d92-8bff-3c471730fe45',
  password='yzKNcnEDXFmB',
  version='2017-02-27')

def main():


"""
    Analyzes content for major keywords.
:param absUrl: Article Url
:returns: list of strings
"""
def keyWords(absUrl):
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
    
