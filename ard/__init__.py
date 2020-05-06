from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = '517c1d83a102b01035afcd73d9930f1d'
app.config['MONGO_URI'] = "mongodb://localhost:27017/amazonReviews"

mongo = PyMongo(app)

from ard import routes