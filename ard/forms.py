from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')	

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Update')
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

class AddProductForm(FlaskForm):
	asin = StringField('ASIN', validators=[DataRequired(), Length(min=2, max=20)])
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=250)])
	customer_rating = StringField('Customer Rating', validators=[DataRequired(), Length(min=1,max=20)])
	price = StringField('Price', validators=[DataRequired(), Length(min=2, max=10)])
	shipping = StringField('Shipping', validators=[DataRequired(), Length(min=2, max=10)])
	sold_by = StringField('Sold By', validators=[DataRequired(), Length(min=2, max=15)])
	color = StringField('Color', validators=[DataRequired(), Length(min=2, max = 15)])
	submit = SubmitField('Add')

class AddCommentForm(FlaskForm):
	review_text = StringField('Review Text', validators=[DataRequired(), Length(min=4, max=300)])
	submit = SubmitField('Add Comment')

class DeleteForm(FlaskForm):
	submit = SubmitField('Delete Product')

class UpdateForm(FlaskForm):
	fieldname = StringField('Field Name', validators=[DataRequired(), Length(min=4, max=100)])
	fieldvalue = StringField('Field Value', validators=[DataRequired(), Length(min=4, max=100)])
	submit = SubmitField('Update Product')


