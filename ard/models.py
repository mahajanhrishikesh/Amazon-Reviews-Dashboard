from ard import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	try:
		return User.query.get(int(user_id))
	except:
		return None

class User(UserMixin):
	
	def __init__(self, email, password, username):
		self.id = None
		self.email = email
		self.password = password
		self.username = username

	def __repr__(self):
		return f"User('{self.username}','{self.email}', '{self.is_authenticated}')"

	def get(self, id):
		return id