from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64))
    password_hash = db.Column(db.String(256), unique=True)
    key = db.Column(db.String(8), unique=True)
    verified = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_verification_key(self, key):
        if self.key == key:
            return True
        else:
            return False

    def set_verified(self, value):
        self.verified = value

class Profile(db.Model):
    owner_id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(256), unique=True)
    status = db.Column(db.String(256), unique=True)

class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(512), unique=True)

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(512), unique=True)
    date = db.Column(db.DateTime)

@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))
