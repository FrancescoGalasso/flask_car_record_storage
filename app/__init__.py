from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from pathlib import Path
import pathlib
from flask_admin import Admin
from .views import MyAdminIndexView, UserModelView, CarModelView

app_flask_car_record_storage = Flask(__name__)
app_flask_car_record_storage.config.from_object(Config)
db = SQLAlchemy(app_flask_car_record_storage)
login = LoginManager(app_flask_car_record_storage)
login.login_view = 'login'

from app import routes, models



admin = Admin(app_flask_car_record_storage, 
			template_mode='bootstrap3',
			index_view=MyAdminIndexView(name='Car Record Storage',
										url='/'))

admin.add_view(UserModelView(models.User, db.session))
admin.add_view(CarModelView(models.Car, db.session))

# Create DB with a test user if DB does not exist
parent_dir = Path(__file__).parent.parent
DB_PATH = parent_dir / 'car_record_storage.db'

if not DB_PATH.exists():

	# create tables
	db.create_all()

	# create some users
	admin_user = models.User(name='admin', email='admin@example.com', password_hash=generate_password_hash('admin'))
	test_user = models.User(name='test_user', email='test_user@example.com', password_hash=generate_password_hash('test_user'))
	db.session.add(admin_user)
	db.session.add(test_user)
	db.session.commit()

if app_flask_car_record_storage.config['POPULATE_SAMPLE_DB']:
	cars = models.Car.query.all()

	if not cars:
		sample_cars= [
			{'name': 'Lancia Ypsilon 2020', 'plate': '123B', 'brand': 'Lancia', 'model':'Ypsilon'},
			{'name': 'Peugeot 307 CC', 'plate': '123A', 'brand': 'Peugeot', 'model':'Coupé-Cabriolet'},
		]

		for sample_car in sample_cars:
			model_car = models.Car(name=sample_car.get('name'), 
									plate=sample_car.get('plate'), 
									brand=sample_car.get('brand'),
									model=sample_car.get('model'))
			db.session.add(model_car)

		db.session.commit()

	
