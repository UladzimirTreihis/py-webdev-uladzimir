from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, InputRequired


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register') 


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In') 


class LogOutForm(FlaskForm):
    submit = SubmitField('Log Out') 