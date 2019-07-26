from flask import Flask,url_for,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

from werkzeug.security import generate_password_hash,check_password_hash

import os



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret strings'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)


    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

class AddMovie(FlaskForm):
    title = StringField('title')
    year = StringField('year')
    submit = SubmitField('Add')

class EditMovie(FlaskForm):
    title = StringField('title')
    year = StringField('year')
    submit = SubmitField('Updata')


class DeleteMovie(FlaskForm):
    submit = SubmitField('Delete')

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user = user)

@app.route('/',methods = ['GET','POST'])
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    form = AddMovie()
    form_delete = DeleteMovie()
    if form.validate_on_submit():
        title = form.title.data
        year = form.year.data
        
        movie = Movie(title = title , year = year)
        db.session.add(movie)
        db.session.commit()

        flash('Add movie ' + title + 'success')
        return redirect(url_for('index'))

    return render_template('index.html' ,form = form,form_delete = form_delete ,movies = movies)

@app.route('/movie/edit/<movie_id>',methods = ['GET','POST'])
def edit(movie_id):
    form = EditMovie()

    movie = Movie.query.get_or_404(movie_id)

    if form.validate_on_submit():

        movie.title = form.title.data
        movie.year = form.year.data
        db.session.commit()
        flash('Item Updated.')
        
        return redirect(url_for('index'))

    return render_template('edit.html',form = form,movie = movie )

@app.route('/movie/delete/<movie_id>',methods = ['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

