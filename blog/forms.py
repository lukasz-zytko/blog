from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from config import Config
from werkzeug.routing import ValidationError

class EntryForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    body = TextAreaField("body", validators=[DataRequired()])
    is_published = BooleanField("is_published", default=False)

class LoginForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired()])
   password = PasswordField('Password', validators=[DataRequired()])

   def validate_username(self, field):
       if field.data != Config.ADMIN_USERNAME:
           raise ValidationError("Niewłaściwy użytkownik")
       return field.data

   def validate_password(self, field):
       if field.data != Config.ADMIN_PASSWORD:
           raise ValidationError("Niewłaściwe hasło")
       return field.data