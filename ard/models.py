from ard import mongo, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	user = mongo.db.User.find_one({"_id": user_id})
	if user is not None:
	    return User(_id=user["_id"])
	else:
	    return None

class User(UserMixin):
	def __init__(self, _id, username, email):
		self.id = _id
		self.username = username
		self.email = email
	

