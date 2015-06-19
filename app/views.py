from app import app, models, db
from .forms import UserForm, QuestionForm
from flask import render_template, redirect, url_for, request, session
from passlib.hash import sha512_crypt
from datetime import datetime

@app.route('/', methods=["GET", "POST"])
def index():
	site_title = 'Questinify'
	if request.method == 'POST':
		if 'logged_in' in session:
			return redirect(url_for('dashboard'))
		else:
			return redirect(url_for('login'))
	return render_template('index.html', site_title=site_title)

@app.route('/about')
def about():
	return "About"

@app.route('/contact')
def contact():
	return "Contact Us"

@app.route('/register', methods=["GET", "POST"])
def register():
	form = UserForm()
	site_title = 'Register'
	error = None
	if request.method == 'POST':
		if form.validate():
			user = models.User(nickname=request.form['nickname'],
								email=request.form['email'],
								passwordhash=request.form['password']
								)
			userdatabase = models.User.query.filter_by(email=request.form['email']).first()
			if userdatabase is None:
				db.session.add(user)
				db.session.commit()
				session['logged_in'] = True
				session['nickname'] = request.form['nickname']
				return redirect(url_for('dashboard'))
			else:
				error = 'Already registered'
		else:
			error = 'Some fields is error'
	return render_template('register.html', 
							site_title=site_title,
							form=form,
							error=error)

@app.route('/login', methods=["GET", "POST"])
def login():
	form = UserForm()
	site_title = 'Login'
	error = None
	if request.method == 'POST':
		if form.validate_on_submit:
			user = models.User.query.filter_by(email=request.form['email']).first()
			if user is not None and sha512_crypt.verify(request.form['password'], user.passwordhash):
				session['logged_in'] = True
				session['nickname'] = user.nickname
				session['uid'] = user.id
				return redirect(url_for('dashboard'))
			else:
				error = 'Invalid username or password.'
	return render_template('login.html',
							form=form,
							site_title = site_title,
							error = error
							)
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.clear()
	return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
	site_title = 'Dashboard'
	if 'logged_in' in session:
		nickname = session['nickname']
		uid = session['uid']
		question = models.Question.query.filter_by(user_id=uid).all()
		return render_template('dashboard.html',
								site_title=site_title,
								nickname=nickname,
								uid=uid,
								question=question
								)
	else:
		return redirect(url_for('login'))

@app.route('/question', methods=['GET','POST'])
def question():
	form = QuestionForm()
	site_title = 'Question'
	error = None
	if 'logged_in' in session:
		if request.method == 'POST' and form.validate_on_submit:
			question = models.Question(question=request.form['question'],
										description=request.form['description'],
										timestamp=datetime.utcnow(),
										user_id=session['uid']
										)
			db.session.add(question)
			db.session.commit()
			return redirect(url_for('dashboard'))
		else:
			error = 'Some fields error'
	else:
		error = 'Please log in first!'

	return render_template('question.html',
							form=form,
							site_title=site_title)
