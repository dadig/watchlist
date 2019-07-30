import os
from watchlist import app

SQLALCHEMY_DATABASE_URI='sqlite:////' + os.path.join(app.root_path,'data.db')
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY='secret strings'
