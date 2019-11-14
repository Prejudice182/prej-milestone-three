# Import required modules
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, validators
from wtforms.validators import InputRequired
from wtforms.widgets import Select, html_params, HTMLString

# Code below taken from https://stackoverflow.com/questions/23460857/create-selectfield-options-with-custom-attributes-in-wtforms


class AttribSelect(Select):
    """
    Renders a select field that supports options including additional html params.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected, html_attribs)`.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for val, label, selected, html_attribs in field.iter_choices():
            html.append(self.render_option(
                val, label, selected, **html_attribs))
        html.append('</select>')
        return HTMLString(''.join(html))


class AttribSelectField(SelectField):
    widget = AttribSelect()

    def iter_choices(self):
        for value, label, render_args in self.choices:
            yield (value, label, self.coerce(value) == self.data, render_args)

    def pre_validate(self, form):
        if self.choices:
            for v, _, _ in self.choices:
                if self.data == v:
                    break
            else:
                raise ValueError(self.gettext('Is Not a valid choice'))
# End code from Stack Overflow


# Define our EntryForm class, inheriting from FlaskForm
class EntryForm(FlaskForm):
    ''' Defines a form to be used for adding a favourite show or movie '''
    entry_name = StringField('Movie / TV Show Name', [InputRequired()])
    entry_type = AttribSelectField('Type', [InputRequired()], choices=[
        ('', 'Please select a type', dict(disabled='disabled')), ('movie', 'Movie', dict()), ('series', 'TV Show', dict())], default='')
    username = StringField('Your Name', [InputRequired()])
    reason = TextAreaField('Reason', [InputRequired()])
    submit = SubmitField('Post Listing')
