from flask import Flask,url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1> Hello Totoro !</h1><img src="watchlist/totoro.gif"/>'

@app.route('/home/')
def home():
    print(url_for('hello'))
    return "Welcom to MY watchlist"

@app.route('/test/<name>')
def test(name):
    return "test: %s" % name
