from flask.ext.wtf import Form 
from wtforms import TextField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, Email

class UserForm(Form):
	nickname = TextField('Nickname', validators=[Required()])
	email = TextField('Email', validators=[Required(), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me', default=False)

class QuestionForm(Form):
	question = TextField('Question', validators=[Required()])
	description = TextAreaField('Description')
	guest = BooleanField('Guest', default=False)
	anonymous = BooleanField('Anonymous', default=False)

class AnswerForm(Form):
	answer = TextAreaField('Answer', validators=[Required()])

class CommentForm(Form):
	comment = TextAreaField('Comment', validators=[Required()])

class GuestForm(Form):
	name = TextField('Name', validators=[Required()])
	email = TextField('Email', validators=[Required(), Email()])
	anonymous = BooleanField('Anonymous', default=False)