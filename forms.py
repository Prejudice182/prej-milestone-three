from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, validators
from wtforms.validators import InputRequired


class EntryForm(FlaskForm):
    entry_name = StringField('Movie / TV Show Name', [InputRequired()])
    entry_type = SelectField('Type', [InputRequired()], choices=[
                            ('', 'Please select a type'), ('movie', 'Movie'), ('series', 'TV Show')])
    username = StringField('Your Name', [InputRequired()])
    reason = TextAreaField('Reason', [InputRequired()])
    submit = SubmitField('Post Listing')
