import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from ard import app, mongo, bcrypt, login_manager
from ard.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from ard.models import User
from flask import session

def setsession():
	session['is_active']=False


@app.route('/home')
def home():
	if session['is_active']==True:
		print(session['username'])
	prods = list(mongo.db.appliances.find().limit(30))
	image_file = url_for('static', filename="images/sentiment_overall.png")
	return render_template('home.html', title='Home', prods=prods, image_file=image_file)

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

@app.route('/', methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = list(mongo.db.Users.find({'email':form.email.data}))[0]
		print(user)
		if user and bcrypt.check_password_hash(user['password'], form.password.data):
			user = User(user['email'], user['password'], user['username'])
			login_user(user, remember = form.remember.data)
			print(current_user)
			session['username'] = current_user.username
			session['email'] = current_user.email
			session['is_active'] = True
			flash(f'You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash(f'Incorrect username password!', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	setsession()
	return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = session['username']
		form.email.data = session['email']
	return render_template('account.html', title='Account', form=form)