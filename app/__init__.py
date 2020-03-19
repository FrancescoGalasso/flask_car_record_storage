from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from pathlib import Path
import pathlib
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

app_flask_car_record_storage = Flask(__name__)
app_flask_car_record_storage.config.from_object(Config)
db = SQLAlchemy(app_flask_car_record_storage)
login = LoginManager(app_flask_car_record_storage)
login.login_view = 'login'

from app import routes, models

class CustomModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inacessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))

	@property
	def can_create(self):
		return current_user.name == 'admin'

	@property
	def can_edit(self):
		return current_user.name == 'admin'

	@property
	def can_delete(self):
		return current_user.name == 'admin'
 
	def is_accessible(self):
		if self.model.__tablename__ == 'user':
			if current_user.name == 'admin':
				return True
			else:
				return False
		else:
			return True

	def is_visible(self):
		if self.model.__tablename__ == 'user':
			if current_user.name == 'admin':
				return True
			else:
				return False
		else:
			return True

	column_exclude_list = ('password_hash', 'modification_time')
	
class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		# redirect to login page if user doesn't have access
		return redirect(url_for('login'))

admin = Admin(app_flask_car_record_storage, 
			template_mode='bootstrap3',
			index_view=MyAdminIndexView(name='Car Record Storage',
										url='/'))

# admin = Admin(app_flask_car_record_storage,
# 				name='Car Record Storage',
# 				template_mode='bootstrap3',
# 				url='/')

admin.add_view(CustomModelView(models.User, db.session))
admin.add_view(CustomModelView(models.Car, db.session))

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

	
