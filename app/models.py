from app import login
from datetime import datetime
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    otdel = db.Column(db.String(64))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    question = db.Column(db.String(500), unique=True)
    user_answers = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Questions(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), unique=True)
    q_type = db.Column(db.String(20))

    def __repr__(self):
        return '<User {}>'.format(self.question)


class Answers(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    answer = db.Column(db.String(64))
    yes_no = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.answer)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
