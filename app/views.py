from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class BaseCustomModelView(ModelView):
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

class UserModelView(BaseCustomModelView):
	column_exclude_list = ('password_hash', 'modification_time')

class CarModelView(BaseCustomModelView):
	column_exclude_list = ('creation_time', 'modification_time')
	column_filters = ('name', 'model', 'plate', 'brand')

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		# redirect to login page if user doesn't have access
		return redirect(url_for('login'))
