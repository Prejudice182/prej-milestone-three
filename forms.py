from wtforms import Form, StringField, IntegerField, validators, SubmitField, DateField, DateTimeField
from wtforms.validators import DataRequired, InputRequired
from datetime import datetime


class ListingsForm(Form):
    film_name = StringField('Film Name', [
        InputRequired(message=('Need to name the film!'))
    ])
    screen_number = IntegerField('Screen Number', [
        DataRequired(message=('That\'s not a number! Try again!'))
    ])
    date_field = DateField('Date', [
        InputRequired(message=('What day is it on?'))
    ], '%Y/%m/%d')
    time_field = DateTimeField('Time', [
        InputRequired(message=('What time is it on?'))
    ], '%I:%M %p')
    submit = SubmitField('Post Listing')
