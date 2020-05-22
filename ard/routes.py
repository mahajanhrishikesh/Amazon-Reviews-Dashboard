import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from ard import app, mongo, bcrypt, login_manager
from ard.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddProductForm, AddCommentForm, DeleteForm, UpdateForm
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
	image_file_2 = url_for('static', filename="images/wc.png")
	csv_file = url_for('static', filename="csvs/Brand_wise_data.csv")
	csv_file_2 = url_for('static', filename='csvs/Category_data.csv')
	return render_template('home.html', title='Home', prods=prods, image_file=image_file, csv_file=csv_file, csv_file_2=csv_file_2, image_file_2=image_file_2)

@app.route('/products')
def products():
	prods = list(mongo.db.appliances.find().limit(30))
	return render_template('products.html', title='Products', prods = prods)

@app.route("/products/<productID>")
def product_profile(productID):
	product = mongo.db.appliances.find_one_or_404({"asin": productID})
	reviews = list(mongo.db.appliances_reviews.find({"asin":productID}, {"_id":0, "reviewText":1, "reviewerName":1}))
	return render_template("product.html",product=product, reviews=reviews)

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
	image_file = url_for('static', filename="images/default.jpg")
	return render_template('account.html', title='Account', form=form, image_file=image_file)

@app.route("/addProduct", methods=['GET', 'POST'])
def addProduct():
	form = AddProductForm()
	product = {}
	if form.validate_on_submit():
		product['asin'] = form.asin.data
		product['name'] = form.name.data
		product['features'] = {"Customer Rating": form.customer_rating.data, "price": form.price.data, "Shipping": form.shipping.data, "Sold By": form.sold_by.data, "Color":form.color.data}
		mongo.db.appliances.insert_one(product)
		flash(f'Product Inserted into DB!', 'success')
		return redirect(url_for('product_profile', productID = form.asin.data))
	return render_template('addProduct.html', title='Add Product', form=form)

@app.route("/network", methods=['GET', 'POST'])
def network():
	iframe = 'https://preview.flourish.studio/2502679/zZM-m91nGmVDVFia-tVA4G5kD0DpllwX_u_A-ObdKOrQOEtM47CVdK6HEU1QlYo9/'
	return render_template('network.html', title='Network', iframe=iframe)

@app.route("/comments/<productID>", methods=['GET', 'POST'])
def addComment(productID):
	form = AddCommentForm()
	review = {}
	if form.validate_on_submit():
		review['reviewText'] = form.review_text.data
		if session['is_active']:
			review['reviewerName'] = session['username']
		else:
			review['reviewerName'] = 'Anonymous'
		review['asin'] = productID
		mongo.db.appliances_reviews.insert_one(review)
		return redirect(url_for('product_profile', productID = productID))
	return render_template('addComment.html', title="Add Commment", form=form)

@app.route("/delete/<productID>", methods=['GET', 'POST'])
def deleteProduct(productID):
	form = DeleteForm()
	if form.validate_on_submit():
		mongo.db.appliances.delete_one({"asin":productID})
		return redirect(url_for('products'))
	return render_template('deleteProduct.html', title="Delete Product", form=form)

@app.route("/update/<productID>", methods=['GET', 'POST'])
def updateProduct(productID):
	form = UpdateForm()
	update={}
	if form.validate_on_submit():
		update[form.fieldname.data] = form.fieldvalue.data
		mongo.db.appliances.update_one({"asin":productID}, {"$set": update})
		print(update)
		return redirect(url_for('product_profile', productID = productID))
	return render_template('updateProduct.html', title="Update Product", form=form)