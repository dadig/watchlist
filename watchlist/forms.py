from wtforms import StringField,SubmitField,PasswordField
from flask_wtf import FlaskForm

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

class Settings(FlaskForm):
    name = StringField('name')
    submit = SubmitField('Update')

class Login_Form(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('submit')

