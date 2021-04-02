from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from app.forms import LoginForm, RegisterForm, VerifyForm, LogoutForm, CreateEventForm
from app import db
from app.models import User, Event
import sys
from random import randint, random, choice
import string

app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "projectsociiteam@gmail.com",
    MAIL_PASSWORD = "projectsociiteamspr21",
    MAIL_DEFAULT_SENDER = ("Project Socii Team", "projectsociiteam@gmail.com"),
    SECRET_KEY = "sociiteamwins")

mail = Mail(app)

def keygen(length): #Generate a key with random numbers and letters.
	key = ""
	for x in range(length):
		nextChar = randint(1, 2)
		if nextChar == 1: #Add an integer to the key.
			key += str(randint(0, 9))
		else: #Add an ASCII character.
			key += choice(string.ascii_uppercase)
	return key

		

def sendverificationmail(recipient, key, phase):
	if phase == 1:
		subject = "Project Socii Account Verification"
		message = "Welcome to Southern Connecticut State University's Project Socii social media platform! To complete your account verification, enter this key on the website: <b>"+ str(key)+"</b>"
		msg = Message(subject, recipients=[recipient], body=message)
	elif phase == 2:
		subject = "Project Socii Account Verification"
		message = "Congratulations! Your account has been successfully verified and is now activated."
		msg = Message(subject, recipients=[recipient], body=message)
	mail.send(msg)

@app.route("/")
def index():
	return render_template("home.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
	if current_user.is_authenticated:
	    print(current_user.username)
	    return redirect(url_for("index"))
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.query(User).filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			print("Login failed!", file=sys.stderr)
			return redirect(url_for("login"))
		login_user(user)
		print("Login successful!", file=sys.stderr)
		if user.verified == False: #The user has not verified their account, ask them to verify before proceeding.
		    return redirect(url_for("verify"))
		else: #The user's account is verified, send them to the homepage.
		    return redirect(url_for("index"))
		   
	return render_template("login.html", form = form)

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for("login"))
    return render_template("logout.html", form=form)

@app.route("/verify", methods = ["GET", "POST"])
def verify():
    form = VerifyForm()
    if current_user.is_authenticated: #Check if the user is logged in first.
        if form.validate_on_submit(): #Check if the form is completed.
            verifiedUser = db.session.query(User).filter_by(username=current_user.username).first() #Find the user attempting to verify in the database.
            if verifiedUser.check_verification_key(form.keycode.data): #Check if the user's input matches their saved verification code.
                print("Account successfully verified.")
                verifiedUser.set_verified(True) #Set their account to verified.
                db.session.add(verifiedUser) #Update this in the database.
                db.session.commit() #Commit the changes.
                sendverificationmail(verifiedUser.email, 0, 2) #Send an email confirming the verification.
                return redirect(url_for("index"))
            else: #The code was incorrect, try again.
                print("That verification code was incorrect.", file=sys.stderr)
                return redirect(url_for("verify"))
    else: #The user is not logged in, send them to the login page.
        return redirect(url_for("login"))
    return render_template("verify.html", form=form)


@app.route("/createaccount", methods = ["GET", "POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		newUser = db.session.query(User).filter_by(username=form.username.data).first()
		if newUser is None: #This username is available.
			newKey = keygen(6) #Generate a random key.
			newUser = User(username = form.username.data, email = form.email.data, role="User", key=newKey) #Add checks here later for username appropriateness and password strength.
			newUser.set_password(form.password.data)
			db.session.add(newUser)
			db.session.commit()
			sendverificationmail(newUser.email, newKey, 1)
			print("User account successfully created.")
			
			return redirect(url_for("verify"))
		else:
			print("This username is already in use.", file=sys.stderr)
			return redirect(url_for("register"))
	return render_template("register.html", form=form)

@app.route('/createevent', methods=['GET', 'POST'])
def createevent():
    form = CreateEventForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        date = form.date.data

        e = Event(name=name, description=description, date=date)

        db.session.add(e)
        db.session.commit()

        form.name.data = ''
        form.description.data = ''
        form.date.data = ''
        return redirect(url_for('createevent'))
    return render_template('createevent.html', form=form)
