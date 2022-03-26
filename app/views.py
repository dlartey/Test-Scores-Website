from flask import render_template, flash, redirect, session, url_for, request, g
from app.forms import LoginForm, ModuleEnrollForm, ModuleForm, PasswordForm, ScoreForm, StudentForm
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from app import app, db, admin
from .models import Student, Module, Scores, enrollment
from werkzeug.security import generate_password_hash, check_password_hash
import logging

admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Module, db.session))
admin.add_view(ModelView(Scores, db.session))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
	return Student.query.get(int(user_id))

@app.route("/")
def homepage():
	app.logger.info('index route request') 
	if current_user.is_anonymous == False:
		app.logger.info('index route request') 
		return redirect(url_for('dashboard'))
	return render_template('index2.html',title='homepage',)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
	username = None
	form = StudentForm()
	if form.validate_on_submit():
		data = Student.query.filter_by(username=form.username.data).first()
		if data is None:
			# If there is no title in the database then add a new one
			hashed = generate_password_hash(form.password_hash.data, "sha256")

			data = Student(username=form.username.data, firstName=form.firstName.data, lastName=form.lastName.data, password_hash=hashed)
			db.session.add(data)
			db.session.commit()
			app.logger.info('%s Registed Successfully', form.username.data)
			flash("Student Added Successfully!")
		else:
			flash("Username is already taken")
		username = form.username.data
		form.firstName.data = ''
		form.firstName.data = ''
		form.lastName.data = ''
		form.password_hash.data = ''

	get_assignments = Student.query.order_by(Student.id)
	return render_template("add_student.html", 
		form=form,
		username=username,
		get_assignments=get_assignments)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		student = Student.query.filter_by(username=form.username.data).first()
		if student:
			if check_password_hash(student.password_hash, form.password_hash.data):
				form.username.data = ''
				form.password_hash.data = ''
				login_user(student)
				flash('Login Successfull')
				app.logger.info('%s logged in  Successfully', form.username.data)
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("User doesn't exist")
			return redirect(url_for('login'))
		
	
	return render_template("login.html",form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	return render_template("dashboard.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	app.logger.info('%s Registed Successfully', current_user.username)
	logout_user()
	flash("You have been logged out")
	return redirect(url_for('login'))

@app.route('/enroll_module', methods=['GET', 'POST'])
@login_required
def enroll_module():
	form = ModuleEnrollForm()
	if form.validate_on_submit():
		for modId in form.modules.data:
			mod = Module.query.get(modId)
			current_user.modules.append(mod)
		db.session.commit()
		flash("Modules successfully enrolled")
		app.logger.info('%s Enrolled in module Successfully', current_user.username)
	
	return render_template("enroll_module.html",form=form)

@app.route('/add_scores', methods=['GET', 'POST'])
@login_required
def add_scores():
	form = ScoreForm()
	if form.validate_on_submit():
		data = Scores(s_id=current_user.id, m_id=form.modules.data, score=form.score.data, date=form.date.data)
		db.session.add(data)
		db.session.commit()
		flash("Test score added")
			
	return render_template("add_scores.html",form=form)


@app.route('/view_score', methods=['GET', 'POST'])
@login_required
def view_score():
	data = Scores.query.filter_by(s_id = current_user.id).first()
	data2 = Module.query.filter_by(id = data.id).first()
	print(data)
	return render_template("view_score.html", scores=current_user.studentScores)

@app.route('/view_modules', methods=['GET', 'POST'])
@login_required
def view_modules():
	return render_template("view_modules.html", modules=current_user.modules)


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
	form = PasswordForm()
	if form.validate_on_submit():
		student = Student.query.filter_by(username=current_user.username).first()
		if student:
				hashed = generate_password_hash(form.password_hash.data, "sha256")

				student.password_hash = hashed
				db.session.commit()
				flash("Password successfully updated!")

		else:
			flash("User doesn't exist")
			return redirect(url_for('login'))
		
	
	return render_template("edit_student.html",form=form)


@app.route('/delete_score/<id>', methods=['GET'])
@login_required
def delete_score(id):
	module = Scores.query.filter_by(m_id=id).first()
	score = module.query.filter_by(s_id=current_user.id).first()
	#print(score)
	db.session.delete(score)
	db.session.commit()
	flash("Score deleted!")
	return redirect('/')
