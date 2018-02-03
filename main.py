from flask import Flask,request, render_template
import datetime
import calendar
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



    startForWatson = calendar.timegm(startFinal.timetuple())
    endForWatson = calendar.timegm(endFinal.timetuple())

    name = str(request.form['text'])
    return start + name + end












if __name__ == "__main__":
    app.run()



def check(start, end, name):
    print(start + end + name)