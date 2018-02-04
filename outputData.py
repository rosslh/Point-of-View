import datetime
import time
import plotly
import plotly.graph_objs as go
import numpy
import scipy


def createAndShowGraph(urls, dates, newstype, scores, keywords, mainKeyword):
    cnnXaxis = []
    cnnYaxis = []
    cnnHover = []
    foxXaxis = []
    foxYaxis = []
    foxHover = []

    for i in range(len(urls) - 1):
        if newstype[i].lower() == "fox":
            if float(scores[i]) != 0:
                foxXaxis.append(datetime.datetime.fromtimestamp(dates[i]))
                foxYaxis.append(float(scores[i]))
                foxHover.append("Article: " + urls[i])
        elif newstype[i].lower() == "cnn":
            if float(scores[i]) != 0:
                cnnXaxis.append(datetime.datetime.fromtimestamp(dates[i]))
                cnnYaxis.append(float(scores[i]))
                cnnHover.append("Article: " + urls[i])

    cnnPoints = go.Scatter(
        x=cnnXaxis,
        y=cnnYaxis,
        mode="markers",
        name="CNN (Averate Sentiment: " + str(sum(cnnYaxis) / float(len(cnnYaxis)))[:8] + ")",
        text=cnnHover
    )

    foxPoints = go.Scatter(
        x=foxXaxis,
        y=foxYaxis,
        mode="markers",
        name="Fox (Average Sentiment: " + str(sum(foxYaxis) / float(len(foxYaxis)))[:8] + ")",
        text=foxHover
    )

    layout = go.Layout(
        title="Analysis of: " + str(mainKeyword) + " from " + time.strftime("%Y-%m-%d", time.gmtime(dates[0])) + " to "
        + time.strftime("%Y-%m-%d", time.gmtime(dates[len(dates) - 1])),
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
            range=[-1, 1]
        )
    )

    data = [cnnPoints, foxPoints]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='CNN vs Fox.html')


def TakeListOfLists(listOfLists):
    urls = []
    dates = []
    newstype = []
    scores = []
    keywords = []
    mainKeyword = ""
    for sublist in listOfLists:
        urls.append(sublist[0])
        dates.append(sublist[1])
        newstype.append(sublist[2])
        mainKeyword = sublist[3]
        scores.append(sublist[4])
        keywords.append(sublist[5])
    createAndShowGraph(urls, dates, newstype, scores, keywords, mainKeyword)


# A list of lists [String: url,TimeStamp: date,String: networkname,String: Target, Float: score,[String]:keywords]
