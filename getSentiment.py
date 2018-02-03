import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, SentimentOptions, KeywordsOptions

import datetime
import re
import sys
import time

from selenium import webdriver

if sys.version_info[0] > 2:
    from urllib.parse import quote_plus, urlparse, parse_qs
    import urllib.parse
else:
    from urllib import quote_plus
    from urlparse import urlparse, parse_qs
    import urllib.parse
# Try to use BeautifulSoup 4 if available, fall back to 3 otherwise.
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

natural_language_understanding = NaturalLanguageUnderstandingV1(
    username='43f96ab3-69a5-4d92-8bff-3c471730fe45',
    password='yzKNcnEDXFmB',
    version='2017-02-27')

def ymdToTimestamp(date):
    return str(int(time.mktime(datetime.datetime.strptime(date, "/%Y/%m/%d/").timetuple())))

def getDataFromFile(keyword):  # [url, date, network, keyword, -2, []]
    out = []
    pattern = re.compile("/20[0-9]{2}/[0-9]{2}/[0-9]{2}/")
    with open("{}.txt".format(keyword), 'r') as f:
        for article in f.read().split("\n"):
            matched = pattern.search(article)
            if matched:
                out.append([article, ymdToTimestamp(matched.group(0)),
                            "fox" if "foxnews.com" in article else "cnn", keyword, None, None])
    return out


def main():
    print(getDataFromFile("James Comey"))
    print(analyzeIn(getDataFromFile("James Comey")))

    '''
    articlesLocation = "/Users/mwrana/Documents/Github_Repositories/QHacks/articles.txt"
    datesLocation = "/Users/mwrana/Documents/Github_Repositories/QHacks/dates.txt"
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

    for i in range(len(articleContent) - 1):
        tempList = [];
        tempList.append(articleContent[i])
        tempList.append(dateContent[i])
        tempList.append(networkList[i])
        tempList.append("Trump")
        tempList.append(None)
        tempList.append(None)
        finalList.append(tempList)

    print(analyzeIn(finalList))
    '''

# A list of lists [String: url,TimeStamp: date,String: networkname,String: Target, Float: score,[String]:keywords]




'''
    Updates the given data of urls with sentiment scores and keywords
:param:A list of lists [String: url,TimeStamp: date,String: networkname,String: Target, Float: score,[String]:keywords]

'''


def analyzeIn(absUrls):

    for absTuple in absUrls:
        print("reading")
        absUrl = absTuple[0]
        try:
            absTuple[4] = analyzeSentiment(absUrl, absTuple[3])
            absTuple[5] = analyzeKeyWords(absUrl)
            fh = open("sampleResult.txt", "a")
            fh.write(absTuple[0] + "," + absTuple[1] + "," + absTuple[2] + "," + absTuple[3] + "," + str(absTuple[4]) + "," + str(absTuple[5]))
            fh.write("\n")
            fh.close
        except Exception:
            pass
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


def analyzeSentiment(absUrl, target):
    response = natural_language_understanding.analyze(
        url=absUrl,
        features=Features(
            sentiment=SentimentOptions(
                targets=[target])))
    return response['sentiment']['targets'][0]['score']


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


main()

