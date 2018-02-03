import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='43f96ab3-69a5-4d92-8bff-3c471730fe45',
  password='yzKNcnEDXFmB',
  version='2017-02-27')

def main():
    articles = ["https://www.cnn.com/2018/02/02/politics/prison-reform-congress-trump/index.html","https://www.cnn.com/2018/02/02/opinions/street-fighter-trump-blunt-force-against-mueller-borger/index.html","https://www.cnn.com/2018/01/31/politics/donald-trump-rod-rosenstein-december-meeting/index.html","https://www.cnn.com/2018/01/31/politics/strzok-fbi-comey-clinton-letter/index.html","https://www.cnn.com/2018/02/02/politics/what-nunes-memo-proves-analysis/index.html"]
    foxart = ["http://www.foxnews.com/politics/2018/02/02/house-memo-states-disputed-dossier-was-key-to-fbi-s-fisa-warrant-to-surveil-members-team-trump.html","http://www.foxnews.com/us/2018/02/02/following-release-house-memo-fbi-director-says-talk-is-cheap-in-letter-to-bureau.html","http://www.foxnews.com/opinion/2018/02/02/doug-schoen-releasing-republican-memo-risks-integrity-our-criminal-justice-system.html","http://www.foxnews.com/politics/2018/02/02/k-t-mcfarland-trump-nominee-for-ambassador-to-singapore-withdraws-nomination.html","http://www.foxnews.com/opinion/2018/02/02/alan-dershowitz-nunes-fisa-memo-deserves-more-investigation-time-for-nonpartisan-commission.html"]
    scores = []
    keywordsL = []
    for i in foxart:
        keywordsL.append(keyWords(i))
        scores.append(analyzeSentiment(i))
    print(keywordsL)

def keyWords(absUrl):
    response = natural_language_understanding.analyze(
        url=absUrl,
        features=Features(
            keywords=KeywordsOptions(
                limit=5)))
    keywords = [i['text'] for i in response['keywords']]
    return keywords
    
def analyzeSentiment(absUrl):
    response = natural_language_understanding.analyze(
    url=absUrl,
    features=Features(
        sentiment=SentimentOptions()))
    return float(response['sentiment']['document']['score'])
 

main()
    
