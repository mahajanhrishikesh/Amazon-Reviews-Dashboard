from flask import render_template, url_for, redirect, flash
from ard import app
from ard.forms import RegistrationForm, LoginForm
from ard import mongo

@app.route('/')
@app.route('/home')
def home():
	prods = list(mongo.db.appliances.find().limit(30))
	return render_template('home.html', title='Home', prods = prods)

@app.route("/home/<productID>")
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
		user['password'] = form.password.data
		mongo.db.Users.insert_one(user)
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = list(mongo.db.Users.find({'email':form.email.data}))[0]
		print(user)
		if form.password.data == user['password']:
			flash(f'You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash(f'Incorrect username password!', 'danger')
	return render_template('login.html', title='Login', form=form)