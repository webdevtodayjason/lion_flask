from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DailyLogForm(FlaskForm):
    achievements = TextAreaField('Achievements', validators=[DataRequired()])
    issues = TextAreaField('Issues')
    opportunities = TextAreaField('Opportunities')
    next_day_tasks = TextAreaField('Next Day Tasks', validators=[DataRequired()])
    submit = SubmitField('Submit')
