from flask import url_for,render_template,redirect,flash
from watchlist import db,app
from watchlist.models import User,Movie

from watchlist.forms import AddMovie,EditMovie,DeleteMovie,Settings,Login_Form
from flask_login import login_user,login_required,logout_user,current_user
from flask_login import LoginManager

login_manager = LoginManager(app)
login_manager.login_view = 'login'
 
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

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

@app.route('/login',methods = ['GET','POST'])
def login():
    
    form  = Login_Form()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        if not username or not password:
            flash('Invalid input!')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('login success')
            return redirect(url_for('index'))

        flash('invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html',form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/movie/edit/<movie_id>',methods = ['GET','POST'])
@login_required
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
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')

    return redirect(url_for('index'))

@app.route('/settings',methods = ['GET','POST'])
@login_required
def settings():
    form = Settings()
    if form.validate_on_submit():
        name = form.name.data
        flash(name)

        if not name :
            flash('Invali input.')
            return redirect(url_for('settings'))
        current_user.name = name
        #user = User.query.first()
        #user.name = name

        db.session.commit()
        flash('Settings Updated.')
        return redirect(url_for('index'))
    return render_template('settings.html', form = form)

