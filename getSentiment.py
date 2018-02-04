from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import (Features,
                                                                      KeywordsOptions,
                                                                      SentimentOptions)

natural_language_understanding = NaturalLanguageUnderstandingV1(
    username='43f96ab3-69a5-4d92-8bff-3c471730fe45',
    password='yzKNcnEDXFmB',
    version='2017-02-27')


def analyzeIn(absUrls):
    for absTuple in absUrls:
        print("reading")
        absUrl = absTuple[0]
        try:
            absTuple[4] = analyzeSentiment(absUrl)
            absTuple[5] = analyzeKeyWords(absUrl)
        except Exception as e:
            print(e)
    return absUrls


def analyzeKeyWords(absUrl):
    """
        Analyzes content for major keywords.
    :param absUrl: Article Url
    :returns: list of strings
    """
    response = natural_language_understanding.analyze(
        url=absUrl,
        features=Features(
            keywords=KeywordsOptions(
                limit=3)))
    keywords = [i['text'] for i in response['keywords']]
    return keywords


def analyzeSentiment(absUrl):
    """
        Analyzes content for general sentiment/tone
    :param absUrl: Article Url
    :returns: floating point value between -1 and 1. -1 being most negative and
              1 being most positive.
    """
    response = natural_language_understanding.analyze(
        url=absUrl,
        features=Features(
            sentiment=SentimentOptions()))
    return response['sentiment']['document']['score']


def cnnVsFoxSentiment(formattedURLS):
    cnnArt = [x[4] for x in formattedURLS if x[2] == 'cnn']
    foxArt = [x[4] for x in formattedURLS if x[2] == 'foxnews']
    cnnAvg = 0
    foxAvg = 0
    try:
        cnnAvg = (sum(cnnArt)) / (len(cnnArt))
    except:
        pass
    try:
        foxAvg = (sum(foxArt)) / (len(foxArt))
    except:
        pass
    return [cnnAvg, foxAvg]
