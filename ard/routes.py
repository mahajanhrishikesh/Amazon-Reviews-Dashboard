import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from ard import app, mongo, bcrypt
from ard.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from ard.models import User



@app.route('/')
@app.route('/home')
def home():
	prods = list(mongo.db.appliances.find().limit(30))
	return render_template('home.html', title='Home', prods = prods)

@app.route('/products')
def products():
	prods = list(mongo.db.appliances.find().limit(30))
	return render_template('products.html', title='Products', prods = prods)

@app.route("/products/<productID>")
def product_profile(productID):
	product = mongo.db.appliances.find_one_or_404({"asin": productID})
	return render_template("product.html",product=product)

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	user = {}
	if form.validate_on_submit():
		user['username'] = form.username.data
		user['email'] = form.email.data
		user['password'] = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		mongo.db.Users.insert_one(user)
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = list(mongo.db.Users.find({'email':form.email.data}))[0]
		print(user)
		if user and bcrypt.check_password_hash(user['password'], form.password.data):
			user_obj = User(_id=user['_id'], username=user['username'], email = user['email'], )
			login_user(user_obj, remember = form.remember.data)
			flash(f'You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash(f'Incorrect username password!', 'danger')
	return render_template('login.html', title='Login', form=form)