from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from application import bcrypt
from flask_login import current_user

class PostForm(FlaskForm):
	name = StringField('name', validators=[DataRequired(), Length(min=4, max=100)])
	submit = SubmitField('next')

class RegistrationForm(FlaskForm):
	first_name = StringField('first name', validators=[DataRequired(), Length(min=2, max=30)])
	last_name = StringField('last name', validators=[DataRequired(), Length(min=2, max=30)])
	email = StringField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('sign up')

	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('email already in use')

class LoginForm(FlaskForm):
	email = StringField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])
	remember = BooleanField('remember me') #this field needs to be called remember
	
	submit = SubmitField('login')
	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError('email not recognised')

	def validate_password(self, password):
		user = Users.query.filter_by(email=self.email.data).first()
		if user:
			if not bcrypt.check_password_hash(user.password,self.password.data):
				raise ValidationError('password not recognised')

class UpdateAccountForm(FlaskForm):
	first_name = StringField('first name', validators=[DataRequired(), Length(min=2, max=30)])
	last_name = StringField('last name', validators=[DataRequired(), Length(min=2, max=30)])
	email = StringField('email', validators=[DataRequired(), Email()])
	submit = SubmitField('confirm')
	delete = SubmitField('delete account')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = Users.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('email already in use')
		# else:
		# 	raise ValidationError('this is already your email address')

	def delete_account(self):
		current_user.delete()

class FlightForm(FlaskForm):
	date = StringField('date of flight: ', validators=[DataRequired(), Length(min=4, max=100)])
	depart = StringField('departure airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_d = StringField('time of departure: ', validators=[DataRequired(),Length(max=5)])
	arrive = StringField('arrival airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_a = StringField('time of arrival: ', validators=[DataRequired(),Length(max=5)])
	time_a_l = StringField('time of arrival (local): ', validators=[DataRequired(),Length(max=5)])
	submit = SubmitField('next')

class AccommodationForm(FlaskForm):
	name = StringField('name of accommodation: ', validators=[DataRequired(), Length(min=4, max=100)])
	address = StringField('address: ', validators=[DataRequired(), Length(min=4, max=100)])
	arr_date = StringField('arrival date: ', validators=[DataRequired(),Length(max=10)])
	in_time = StringField('check-in time: ', validators=[DataRequired(), Length(max=10)])
	out_date = StringField('leaving date: ', validators=[DataRequired(),Length(max=10)])
	out_time = StringField('check-out time: ', validators=[DataRequired(),Length(max=10)])
	comments = StringField('other info: ', validators=[DataRequired(), Length(max=100)])
	submit = SubmitField('next')

class ActivitiesForm(FlaskForm):
	name = StringField('name of activity: ', validators=[DataRequired(), Length(min=4, max=100)])
	location = StringField('location: ', validators=[DataRequired(), Length(min=4, max=100)])
	date = StringField('date: ', validators=[DataRequired(),Length(max=10)])
	start = StringField('start time: ', validators=[DataRequired(), Length(max=10)])
	end = StringField('end time: ', validators=[DataRequired(),Length(max=10)])
	comments = StringField('other info: ', validators=[DataRequired(), Length(max=100)])
	submit = SubmitField('finish')
	another = SubmitField('add another activity')
	cancel = SubmitField('cancel')