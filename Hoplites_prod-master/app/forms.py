from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = TextField("Username", validators = [DataRequired()])
	password = PasswordField("Password", validators = [DataRequired()])
	submit = SubmitField("Sign in")

class RegisterForm(FlaskForm):
	username = TextField("Username", validators = [DataRequired()])
	email = StringField("Email Address", validators = [DataRequired()])
	password = PasswordField("Password", validators = [DataRequired()])
	submit = SubmitField("Create Account")

class VerifyForm(FlaskForm):
	keycode = TextField("Verification Code", validators = [DataRequired()])
	submit = SubmitField("Verify Account")

class LogoutForm(FlaskForm):
	submit = SubmitField("Sign Out")

class CreateEventForm(FlaskForm):
    name = TextField("Event Name", validators = [DataRequired()])
    description = TextField("Description", validators = [DataRequired()])
    date = TextField("Date", validators = [DataRequired()])
    submit = SubmitField("Create Event")
