from flask import Flask
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config.from_pyfile('setting.py')


db = SQLAlchemy(app)

 

from watchlist.forms import AddMovie,EditMovie,DeleteMovie,Settings,Login_Form
from watchlist import views,errors
