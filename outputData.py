import datetime
import time

import numpy
from numpy import array
from scipy import stats

import plotly
import plotly.graph_objs as go


def createAndShowGraph(urls, dates, newstype, scores, keywords, mainKeyword, source1,  source2):
    cnnXaxis = []
    cnnYaxis = []
    cnnHover = []
    foxXaxis = []
    foxYaxis = []
    foxHover = []
    foxXdata = []
    cnnXdata = []
    for i in range(len(urls) - 1):
        if newstype[i].lower() == source2.lower():
            if float(scores[i]) != 0:
                foxXaxis.append(datetime.datetime.fromtimestamp(dates[i]))
                foxXdata.append(dates[i])
                foxYaxis.append(float(scores[i]))
                foxHover.append("Article: " + urls[i])
        elif newstype[i].lower() == source1.lower():
            if float(scores[i]) != 0:
                cnnXaxis.append(datetime.datetime.fromtimestamp(dates[i]))
                cnnXdata.append(dates[i])
                cnnYaxis.append(float(scores[i]))
                cnnHover.append("Article: " + urls[i])

    foxNumpyIntArray = array([numpy.int64(x) for x in foxXdata])
    cnnNumpyIntArray = array([numpy.int64(x) for x in cnnXdata])

    fslope, fintercept, fr_value, fp_value, fstd_err = stats.linregress(foxNumpyIntArray, foxYaxis)
    cslope, cintercept, cr_value, cp_value, cstd_err = stats.linregress(cnnNumpyIntArray, cnnYaxis)

    fline = fslope * foxNumpyIntArray + fintercept
    cline = cslope * cnnNumpyIntArray + cintercept

    cnnPoints = go.Scatter(
        x=cnnXaxis,
        y=cnnYaxis,
        mode="markers",
        marker=go.Marker(color='blue'),
        name=source1 + " (Average: " + str(sum(cnnYaxis) / float(len(cnnYaxis)))[:8] + ")",
        text=cnnHover
    )

    cnnLine = go.Scatter(
        x=cnnXaxis,
        y=cline,
        mode='lines',
        marker=go.Marker(color='blue'),
        name=source1 + ' Linear Regression Model'
    )

    foxPoints = go.Scatter(
        x=foxXaxis,
        y=foxYaxis,
        mode="markers",
        marker=go.Marker(color='orange'),
        name=source2 + " (Average: " + str(sum(foxYaxis) / float(len(foxYaxis)))[:8] + ")",
        text=foxHover
    )

    foxLine = go.Scatter(
        x=foxXaxis,
        y=fline,
        mode='lines',
        marker=go.Marker(color='orange'),
        name=source2 + ' Linear Regression Model'
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

    data = [cnnPoints, foxPoints, cnnLine, foxLine]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename="comparison.html")


def TakeListOfLists(listOfLists, source1, source2):
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
    createAndShowGraph(urls, dates, newstype, scores, keywords, mainKeyword, source1, source2)


# A list of lists [String: url,TimeStamp: date,String: networkname,String: Target, Float: score,[String]:keywords]
