from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app_flask_car_record_storage, db
from app.forms import LoginForm
from app.models import User


@app_flask_car_record_storage.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('admin/myindex.html')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(name=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=False)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = '/'
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app_flask_car_record_storage.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))