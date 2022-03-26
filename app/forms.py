from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, DateTimeField, PasswordField, BooleanField, DateField, TextAreaField, SelectMultipleField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from .models import Student, Module, Scores
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


class StudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")
   

class ModuleForm(FlaskForm):
    title = StringField('Module Name', validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class ModuleEnrollForm(FlaskForm):
    choices = [(g.id, g.title) for g in Module.query.order_by('title')]
    modules =  SelectMultipleField('modules', coerce=int ,choices = choices)
    submit = SubmitField("Submit")

class ScoreForm(FlaskForm):
    choices = [(g.id, g.title) for g in Module.query.order_by('title')]
    modules =  SelectField('Module Name', coerce=int ,choices = choices)
    score = IntegerField('Score achieved', validators=[DataRequired()])
    date = DateTimeField("Date of Test", validators=[DataRequired()], default=datetime.utcnow)
    submit = SubmitField("Submit")