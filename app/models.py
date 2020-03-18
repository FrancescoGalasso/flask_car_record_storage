from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.inspection import inspect  # pylint: disable=import-error


class BaseModel(db.Model):
    # This is an abstract class: SQLAlchemy will not create a table for that model!
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modification_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @property
    def get_str_time(self):
        return self.creation_time.strftime('%B %d %Y - %H:%M:%S')

    @property
    def object_to_dict(self):

        data = {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

        for k in data.keys():
            if isinstance(data[k], datetime):
                data[k] = data[k].strftime('%B %d %Y - %H:%M:%S')

        return data

class NameModel(BaseModel):
    __abstract__ = True
    name = db.Column(db.String(120), index=True, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

class User(UserMixin, NameModel):
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
