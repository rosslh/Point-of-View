import calendar
import datetime

from findArticles import getDataFromFile, scrapeArticleLinks
from flask import Flask, render_template, request
from getSentiment import analyzeIn
from outputData import TakeListOfLists

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('qHack.html')


@app.route('/', methods=['POST'])
def my_form_post():
    start = request.form['start']
    end = request.form['finish']
    startTime = [int(a) for a in str(start).split('-')]
    startFinal = datetime.datetime(startTime[0], startTime[1], startTime[2], 0, 0)
    endTime = [int(a) for a in str(end).split('-')]
    endFinal = datetime.datetime(endTime[0], endTime[1], endTime[2], 0, 0)

    start_final = calendar.timegm(startFinal.timetuple())
    end_final = calendar.timegm(endFinal.timetuple())

    topic = str(request.form['text'])
    # find articles
    scrapeArticleLinks(topic, start_final, end_final, 7, source1, source2)
    # format as list and get sentiment
    TakeListOfLists(analyzeIn(getDataFromFile(topic, start_final, end_final)))
    # output as graph
    return "start: {}, end: {}, topic: {}".format(start, end, topic)


if __name__ == "__main__":
    app.run()


def check(start, end, name):
    print(start + end + name)
