from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users, Posts
from application import bcrypt, login_manager, app
from flask_login import current_user
# hello
# @app.context_processor
# def login_fix():
# 	import flask_login
# 	return dict(current_user=flask_login._get_user() or current_app.login_manager.anonymous_user())

@login_manager.user_loader #gets id from session
def load_user(id):
	return Users.query.get(int(id))

class PostForm(FlaskForm):
	name = StringField('name', validators=[DataRequired(), Length(min=4, max=100)])
	submit = SubmitField('next')
	def validate_name(self, name):
		post = Posts.query.filter_by(name=name.data).first()
		if post:
			raise ValidationError('name already in use')

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
	first_name = StringField('first name: ', validators=[DataRequired(), Length(min=2, max=30)])
	last_name = StringField('last name: ', validators=[DataRequired(), Length(min=2, max=30)])
	email = StringField('email: ', validators=[DataRequired(), Email()])
	submit = SubmitField('confirm')
	delete = SubmitField('delete account')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = Users.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('email already in use')
		# else:
		# 	raise ValidationError('this is already your email address')

	# def delete_account(self):
	# 	current_user.delete()

class FlightForm(FlaskForm):
	
	cycle = []
	holiday1 = SelectField('Your Trip: ', choices=cycle)
	date1 = StringField('date of flight: ', validators=[DataRequired()])
	depart = StringField('departure airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_d = StringField('time of departure: ', validators=[DataRequired()])
	arrive = StringField('arrival airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_a = StringField('time of arrival: ', validators=[DataRequired()])
	time_a_l = StringField('time of arrival (local): ', validators=[DataRequired()])
	date2 = StringField('date of flight: ', validators=[DataRequired()])
	depart1 = StringField('departure airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_d1 = StringField('time of departure: ', validators=[DataRequired()])
	arrive1 = StringField('arrival airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_a1 = StringField('time of arrival: ', validators=[DataRequired()])
	time_a_l1 = StringField('time of arrival (local): ', validators=[DataRequired()])

	submit = SubmitField('next')

	# def add_choices(request):
	# 	posts = Posts.query.filter_by(author=current_user)
	# 	form = FlightForm(request.POST, obj=posts)
	# 	form.holiday1.choices = [i for i in posts]
		

class AccommodationForm(FlaskForm):
	cycle = []
	holiday1 = SelectField('Your Trip: ', choices=cycle)
	name = StringField('name of accommodation: ', validators=[DataRequired(), Length(min=4, max=100)])
	address = StringField('address: ', validators=[DataRequired(), Length(min=4, max=100)])
	arr_date = StringField('arrival date: ', validators=[DataRequired(),Length(max=10)])
	in_time = StringField('check-in time: ', validators=[DataRequired(), Length(max=10)])
	out_date = StringField('leaving date: ', validators=[DataRequired(),Length(max=10)])
	out_time = StringField('check-out time: ', validators=[DataRequired(),Length(max=10)])
	comments = StringField('other info: ', validators=[Length(max=100)])
	submit = SubmitField('next')

class ActivitiesForm(FlaskForm):
	cycle = []
	holiday1 = SelectField('Your Trip: ', choices=cycle)
	name = StringField('name of activity: ', validators=[DataRequired(), Length(min=4, max=100)])
	location = StringField('location: ', validators=[DataRequired(), Length(min=4, max=100)])
	date = StringField('date: ', validators=[DataRequired(),Length(max=10)])
	start = StringField('start time: ', validators=[DataRequired(), Length(max=10)])
	end = StringField('end time: ', validators=[DataRequired(),Length(max=10)])
	comments = StringField('other info: ', validators=[Length(max=100)])
	submit = SubmitField('finish')
	another = SubmitField('add another activity')
	cancel = SubmitField('cancel')

class EditForm(FlaskForm):
	date1 = StringField('date of flight: ', validators=[DataRequired()])
	depart = StringField('departure airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_d = StringField('time of departure: ', validators=[DataRequired()])
	arrive = StringField('arrival airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_a = StringField('time of arrival: ', validators=[DataRequired()])
	time_a_l = StringField('time of arrival (local): ', validators=[DataRequired()])
	date2 = StringField('date of flight: ', validators=[DataRequired()])
	depart1 = StringField('departure airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_d1 = StringField('time of departure: ', validators=[DataRequired()])
	arrive1 = StringField('arrival airport: ', validators=[DataRequired(), Length(min=4, max=100)])
	time_a1 = StringField('time of arrival: ', validators=[DataRequired()])
	time_a_l1 = StringField('time of arrival (local): ', validators=[DataRequired()])
	
	name = StringField('name of accommodation: ', validators=[DataRequired(), Length(min=4, max=100)])
	address = StringField('address: ', validators=[DataRequired(), Length(min=4, max=100)])
	arr_date = StringField('arrival date: ', validators=[DataRequired(),Length(max=10)])
	in_time = StringField('check-in time: ', validators=[DataRequired(), Length(max=10)])
	out_date = StringField('leaving date: ', validators=[DataRequired(),Length(max=10)])
	out_time = StringField('check-out time: ', validators=[DataRequired(),Length(max=10)])
	comments = StringField('other info: ', validators=[Length(max=100)])

	a1_name1 = StringField('name of activity: ', validators=[DataRequired(), Length(min=4, max=100)])
	a1_location = StringField('location: ', validators=[DataRequired(), Length(min=4, max=100)])
	a1_date = StringField('date: ', validators=[DataRequired(),Length(max=10)])
	a1_start = StringField('start time: ', validators=[DataRequired(), Length(max=10)])
	a1_end = StringField('end time: ', validators=[DataRequired(),Length(max=10)])
	a1_comments1 = StringField('other info: ', validators=[Length(max=100)])
	delete_a1 = SubmitField('delete activity 1')

	a2_name1 = StringField('name of activity: ', validators=[DataRequired(), Length(min=4, max=100)])
	a2_location = StringField('location: ', validators=[DataRequired(), Length(min=4, max=100)])
	a2_date = StringField('date: ', validators=[DataRequired(),Length(max=10)])
	a2_start = StringField('start time: ', validators=[DataRequired(), Length(max=10)])
	a2_end = StringField('end time: ', validators=[DataRequired(),Length(max=10)])
	a2_comments1 = StringField('other info: ', validators=[Length(max=100)])
	delete_a2 = SubmitField('delete activity 2')

	a3_name1 = StringField('name of activity: ', validators=[DataRequired(), Length(min=4, max=100)])
	a3_location = StringField('location: ', validators=[DataRequired(), Length(min=4, max=100)])
	a3_date = StringField('date: ', validators=[DataRequired(),Length(max=10)])
	a3_start = StringField('start time: ', validators=[DataRequired(), Length(max=10)])
	a3_end = StringField('end time: ', validators=[DataRequired(),Length(max=10)])
	a3_comments1 = StringField('other info: ', validators=[Length(max=100)])
	delete_a3 = SubmitField('delete activity 3')

	submit = SubmitField('submit')
	delete = SubmitField('delete trip')    
