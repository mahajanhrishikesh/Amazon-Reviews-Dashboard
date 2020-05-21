from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '517c1d83a102b01035afcd73d9930f1d'
app.config['MONGO_URI'] = "mongodb://localhost:27017/amazonReviews"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

mongo = PyMongo(app)

from ard import routes