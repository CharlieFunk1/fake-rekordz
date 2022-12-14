from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=False)
    message = db.Column(db.String(500), index=False, unique=False)
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(120), index=False, unique=False)
    artistname = db.Column(db.String(64), index=True, unique=False)
    artistemail = db.Column(db.String(120), index=True, unique=False)
    trackname = db.Column(db.String(120), index=True, unique=False)
    albumart = db.Column(db.String(120), index=True, unique=False)
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    

    def __repr__(self):
        return '<Title {} Description {} Artistname {} Artistemail {} Trackname {} Albumart {} Datetime {}>'.format(self.title,
                                                                                            self.description,
                                                                                            self.artistname,
                                                                                            self.artistemail,
                                                                                            self.trackname,
                                                                                            self.albumart,
                                                                                            self.datetime)

class Listen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(120), index=False, unique=False)
    artistname = db.Column(db.String(64), index=True, unique=False)
    artistemail = db.Column(db.String(120), index=True, unique=False)
    trackname = db.Column(db.String(120), index=True, unique=False)
    albumart = db.Column(db.String(120), index=True, unique=False)
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    

    def __repr__(self):
        return '<Title {} Description {} Artistname {} Artistemail {} Trackname {} Albumart {} Datetime {}>'.format(self.title,
                                                                                            self.description,
                                                                                            self.artistname,
                                                                                            self.artistemail,
                                                                                            self.trackname,
                                                                                            self.albumart,
                                                                                            self.datetime)
