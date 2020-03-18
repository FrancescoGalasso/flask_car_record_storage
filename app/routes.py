from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app_flask_car_record_storage, db
# from app.forms import LoginForm, RegistrationForm
from app.models import User

@app_flask_car_record_storage.route('/')
@app_flask_car_record_storage.route('/index')
def index():
	return render_template('index.html')
