import plotly
import plotly.graph_objs as go
import urllib.request
import random
import datetime


def createAndShowGraph(urls,dates,newstype,scores,keywords):

    cnnXaxis = []
    cnnYaxis = []
    cnnHover = []
    foxXaxis = []
    foxYaxis = []
    foxHover = []

    for i in range(len(urls)-1):
        if newstype[i] == "fox" :
            if float(scores[i]) != 0:
                foxXaxis.append(datetime.datetime.fromtimestamp(dates[i]))
                foxYaxis.append(float(scores[i]))
                foxHover.append("Article: " + urls[i])
        elif newstype[i] == "cnn":
            if float(scores[i]) != 0:
                cnnXaxis.append(datetime.datetime.fromtimestamp(dates[i]))
                cnnYaxis.append(float(scores[i]))
                cnnHover.append("Article: " + urls[i])

    print(sum(cnnYaxis) / float(len(cnnYaxis)))
    print(sum(foxYaxis) / float(len(foxYaxis)))

    cnnPoints = go.Scatter(
        x = cnnXaxis,
        y = cnnYaxis,
        mode = "markers",
        name = "CNN",
        text = cnnHover
    )

    foxPoints = go.Scatter(
        x = foxXaxis,
        y = foxYaxis,
        mode = "markers",
        name = "Fox",
        text = foxHover
    )

    layout = go.Layout(
        title = "Analysis of: " + "keywords" + " from " + "startDate" + " to " + "endDate",
        xaxis=dict(
            title='Date',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
            ),
            showticklabels=True,
            tickfont=dict(
                family='Courier New, sans-serif',
                size=14,
                color='black'
            ),
        ),
        yaxis=dict(
            zeroline=True,
            title='Sentiment Score',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
            ),
            showticklabels=True,
            tickfont=dict(
                family='Courier New, sans-serif',
                size=14,
                color='black'
            ),
            range=[-1,1]
        )
    )

    data = [cnnPoints,foxPoints]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='CNN vs Fox.html')

dataLocation = "/Users/mwrana/PycharmProjects/New/sampleResult.txt"

urls = []
dates = []
newstype = []
scores = []
keywords = []


with open(dataLocation) as f:
    line = f.readline().strip()
    while line:
        lineSplit = line.split(",")
        urls.append(lineSplit[0])
        dates.append(int(lineSplit[1]))
        newstype.append(lineSplit[2])
        scores.append(lineSplit[4])
        numKeywords = len(lineSplit)-5
        tempWords = []
        for i in range(numKeywords):
            tempWords.append(lineSplit[len(lineSplit)-1-i].replace("\'","").replace("[","").replace("]","").replace("\n",""))
        keywords.append(tempWords)
        line = f.readline()


createAndShowGraph(urls,dates,newstype,scores,keywords)