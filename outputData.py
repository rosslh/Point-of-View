import plotly
import plotly.graph_objs as go
import urllib.request
import random


def createAndShowGraph(cnnSentiment,foxSentiment,keyWords):

    #Actually fill this array correctly

    points1 = go.Scatter(
        x = [i for i in range(len(cnnSentiment))],
        y = cnnSentiment,
        mode = "lines+markers",
        name = "CNN"
    )

    points2 = go.Scatter(
        x = [i for i in range(len(foxSentiment))],
        y = foxSentiment,
        mode = "lines+markers",
        name = "Fox"
    )

    data = [points1,points2]
    plotly.offline.plot(data, filename='CNN vs Fox.html')

cnnValues = [0.145818, 0.188951, -0.13853, -0.379094, -0.311741]
foxValues = [-0.12272, 0.0675951, -0.344402, -0.40153, -0.397371]
createAndShowGraph(cnnValues,foxValues,"a")