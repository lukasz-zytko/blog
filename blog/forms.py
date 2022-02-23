from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    body = TextAreaField("body", validators=[DataRequired()])
    is_published = BooleanField("is_published", default=False)

