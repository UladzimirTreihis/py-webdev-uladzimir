from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, InputRequired

class AddPostForm(FlaskForm):
    content = StringField('What do you want to tweet today?', validators=[DataRequired()])
    submit = SubmitField('Submit')
