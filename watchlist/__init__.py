from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

movies = Movie.query.all()

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user = user)

@app.route('/')
def index():
    return render_template('index.html' ,movies = movies)

@app.route('/home/')
def home():
    print(url_for('hello'))
    return "Welcom to MY watchlist"

@app.route('/test/<name>')
def test(name):
    return "test: %s" % name

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

