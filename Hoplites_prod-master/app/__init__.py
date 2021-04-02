from flask import Flask

from flask_login import LoginManager
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)

db = SQLAlchemy(app)

load_dotenv('.flaskenv')
PASSWORD = os.environ.get('DATABASE_PASSWORD')
USERNAME = os.environ.get('DATABASE_USERNAME')
DB_NAME = os.environ.get('DATABASE_NAME')

app.config['SECRET_KEY'] = 'HOPLITESPROJECTSPR21'
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://"
                                        + USERNAME
                                        + ":"
                                        + PASSWORD
                                        + "@db4free.net/"
                                        +DB_NAME)

app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"]=True

login = LoginManager(app)

login.login_view = 'login'

from app import routes, models
from app.models import User

db.create_all()

user = User.query.filter_by(username="admin").first()
if user is None:
    userAdmin = User(username="admin", role="admin")
    userAdmin.set_password("sociiadmin1234")
    db.session.add(userAdmin)
    db.session.commit()

user = User.query.filter_by(username="user").first()
if user is None:
    regUser = User(username="user", role="user")
    regUser.set_password("sociiuser1234")
    db.session.add(regUser)
    db.session.commit()
