from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from datetime import datetime
from pathlib import Path
import pathlib
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app_flask_car_record_storage = Flask(__name__)
app_flask_car_record_storage.config.from_object(Config)
db = SQLAlchemy(app_flask_car_record_storage)
login = LoginManager(app_flask_car_record_storage)
login.login_view = 'login'

from app import routes, models

admin = Admin(app_flask_car_record_storage,
				name='Car Record Storage',
				template_mode='bootstrap3', 
				url='/')

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Car, db.session))
# Create DB with a test user if DB does not exist

parent_dir = Path(__file__).parent.parent
DB_PATH = parent_dir / 'car_record_storage.db'

if not DB_PATH.exists():

	# create tables
	db.create_all()

	# create test_user
	admin_user = models.User(name='admin', email='admin@example.com', password_hash=generate_password_hash('admin'))
	db.session.add(admin_user)
	db.session.commit()

# if app_flask_car_record_storage.config['POPULATE_SAMPLE_DB']:
# 	example_car_1 = models.Car(name='Lancia Ypsilon 2020', plate='123B', brand='Lancia', model='Ypsilon')
# 	example_car_2 = models.Car(name='Peugeot 307 CC', plate='123A', brand='Peugeot', model='Coupé-Cabriolet')
# 	db.session.add(example_car_1)
# 	db.session.add(example_car_2)
# 	db.session.commit()

	
