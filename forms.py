from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired

class RegisterUser(FlaskForm):
    """User Registration Form"""
    username = StringField("Username")
    password = PasswordField("Password")
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")

class LoginUser(FlaskForm):
    """User Login Form"""
    username = StringField("Username")
    password = PasswordField("Password")

class FeedBackForm(FlaskForm):
    """User Feedback Form"""
    title = StringField('Title')
    content = TextAreaField('Content')

