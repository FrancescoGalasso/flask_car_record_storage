from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app_flask_car_record_storage = Flask(__name__)
app_flask_car_record_storage.config.from_object(Config)
db = SQLAlchemy(app_flask_car_record_storage)
login = LoginManager(app_flask_car_record_storage)
login.login_view = 'login'

from app import routes, models

# Create DB with a test user if DB does not exist
from pathlib import Path
import pathlib
parent_dir = Path(__file__).parent.parent
DB_PATH = parent_dir / 'car_record_storage.db'

if not DB_PATH.exists():
	from werkzeug.security import generate_password_hash
	from datetime import datetime
	import os

	print('CREATING SAMPLE DB')
	# create tables
	db.create_all()

	# create test_user
	admin_user = models.User(name='admin', email='admin@example.com', password_hash=generate_password_hash('admin'))
	db.session.add(admin_user)

	example_car = models.Car(name='Lancia Ypsilon 2020', plate='123B', brand='Lancia', model='Ypsilon')
	db.session.add(example_car)
	
	db.session.commit()
	
