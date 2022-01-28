# this page is for laying out form objects
# that describe the fields of my forms
# the types of data in my forms
# and any restrictions or validations needed by my forms
from calendar import month
import datetime as dt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

DATE_FORMAT = '%Y-%m-%d'

class signupForm(FlaskForm):
    # having done the inheritence - what we put inside this class is just the fields that we want on our form
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField()


class signinForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()

class updateUsernameForm(FlaskForm):
    newusername = StringField('New Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change Username') 

class historicalRatesForm(FlaskForm):
    base = SelectField('Base Currency', choices = [])
    rate = SelectField('Rate Currency', choices = [])
    date_from = DateField('From Date', format=DATE_FORMAT, validators = [DataRequired(message='Please select from date')])
    date_to = DateField('To Date', format=DATE_FORMAT, validators = [DataRequired(message='Please select to date')])
    submit = SubmitField('Get Rates')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.base.data = 'USD'
        # self.rate.data = 'EUR'
        # self.date_from.data = dt.date.today() - dt.timedelta(days=30)
        # self.date_to.data = dt.date.today()


class currentRatesForm(FlaskForm):
    base = SelectField('Base Currency', choices = [])
    rate = SelectMultipleField('Rate Currency', choices = [])
    submit = SubmitField('Get Rates')