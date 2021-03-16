"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, SelectField, BooleanField, PasswordField


class RegisterForm(FlaskForm):
    """Form for registering user"""

    username = StringField("Username")
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[Length(3), InputRequired()])
    # email = Email()
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in user"""

    username = StringField("Username")
    password = PasswordField("Password", validators=[InputRequired()])

class NewNoteForm(FlaskForm):
    """Form for creating a new note"""

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])


class UpdateNoteForm(FlaskForm):
    """Form for updating a new note"""

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])


