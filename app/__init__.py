from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from pathlib import Path
import pathlib
from flask_admin import Admin
from .views import MyAdminIndexView, UserModelView, CarModelView, CarBrandModelView, CarModelsModelView
from flask_admin.menu import MenuLink


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
admin.add_view(CarBrandModelView(models.CarBrand, db.session))
admin.add_view(CarModelsModelView(models.CarModel, db.session))

class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated             

admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))

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
	brands = models.CarBrand.query.all()

	if not cars and not brands:
		sample_db = {
			'car_brand': [
				{'id': 1, 'name': 'Ferrari'},
				{'id': 2, 'name': 'Lamborghini'}
			],
			'car_model': [
				{'name': 'Testarossa', 'car_brand_id': 1},
				{'name': 'Enzo', 'car_brand_id': 1},
				{'name': 'Diablo', 'car_brand_id': 2},
				{'name': 'Gallardo', 'car_brand_id': 2},
			]
		}

		for car_brand in sample_db.get('car_brand'):
			car_brand_obj = models.CarBrand(id=car_brand.get('id'),
										name=car_brand.get('name'))
			db.session.add(car_brand_obj)

		for car_model in sample_db.get('car_model'):
			car_model_obj = models.CarModel(name=car_model.get('name'),
										car_brand_id=car_model.get('car_brand_id'))
			db.session.add(car_model_obj)

		db.session.commit()

