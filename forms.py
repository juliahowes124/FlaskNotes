"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email
from wtforms import StringField, SelectField, BooleanField, PasswordField


class RegisterForm(FlaskForm):
    """Form for registering user"""

    username = StringField("Username")
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    # email = Email()
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in user"""

    username = StringField("Username")
    password = PasswordField("Password", validators=[InputRequired()])
