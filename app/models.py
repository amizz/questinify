from . import db
from passlib.hash import sha512_crypt as s5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordhash = db.Column(db.String(180), nullable=False)
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')

    def __init__(self, nickname, email, passwordhash):
        self.nickname = nickname
        self.email = email
        self.passwordhash = s5.encrypt(passwordhash)

    def __repr__(self):
        return '<User %r>' % self.email

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))

    #def __init__(self, question, description, timestamp):
    #   self.question = question
    #    self.description = description

    def __repr__(self):
        return '<Question %r>' % self.question

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Anser %r>' % self.answer