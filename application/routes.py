from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Posts, Users, Flights, Accommodation, Activities
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm, FlightForm, AccommodationForm, ActivitiesForm
from flask_login import login_user, current_user, logout_user, login_required
# login user makes and maintains a session for the logged in user
# current user checks if authenticated - authenticated, active, can get id
# logout user removes the user session from being logged in
# login required forces user to be logged in

@app.route('/')
@app.route('/home')
def home():
	# postData = Posts.query.all()
	return render_template('home.html', title='home')

@app.route('/about')
def about():
	return render_template('about.html', title='about')

@app.route('/login', methods=['GET','POST']) #pull & push
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data): #decodes stored password and compares to inputted password
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
	return render_template('login.html', title='login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data)
		user = Users(
			first_name=form.first_name.data,
			last_name=form.last_name.data,
			email=form.email.data,
			password=hashed_pw
			)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('post'))
	return render_template('register.html', title='register', form=form)

@app.route('/post', methods=['GET','POST'])
@login_required
def post():
	form = PostForm()
	if form.validate_on_submit():
		postData = Posts(
			name=form.name.data,
			author=current_user
			)
		db.session.add(postData)
		db.session.commit()
		
		alltheposts=Posts().query.all()
		return redirect(url_for('flights'))
		return render_template('post.html', title='post', form=form, posts=alltheposts)
	else:
		print(form.errors)
		return render_template('post.html', title='post', form=form)
	


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.delete.data:
		#user = User.query.filter(current_user)
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		posts = Posts.query.filter_by(user_id=current_user.id).all()
		for i in posts:
			db.session.delete(i)
		db.session.delete(current_user)
		db.session.commit()
		logout_user()
		return redirect(url_for('login'))
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.email = form.email.data
		db.session.commit()
		return redirect(url_for('account'))
	
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.email.data = current_user.email
	

	return render_template('account.html', title='Account', form=form)

@app.route('/flights', methods=['GET','POST'])
@login_required
def flights():
	holidays = []
	posts = Posts.query.filter_by(user_id=1)
	for post in posts:
		holidays.append(post.name)
	form = FlightForm(request.form)
	if form.validate_on_submit():
		flightData = Flights(
			date = form.date.data,
			depart = form.depart.data,
			time_d = form.time_d.data,
			arrive = form.arrive.data,
			time_a = form.time_a.data,
			time_a_l = form.time_a_l.data,
			date1 = form.date1.data,
			depart1 = form.depart1.data,
			time_d1 = form.time_d1.data,
			arrive1 = form.arrive1.data,
			time_a1 = form.time_a1.data,
			time_a_l1 = form.time_a_l1.data,
			author = current_user,
			holiday1 = form.holiday1.data
		)
		db.session.add(flightData)
		db.session.commit()
		return redirect(url_for('accommodation'))
		return render_template('flights.html', title='flights', form=form, flights=flightData, holidays=holidays)
	else:
		print(form.errors)
		print(form.holiday1.data)
		return render_template('flights.html', title='flights', form=form, holidays=holidays)

@app.route('/accommodation', methods=['GET','POST'])
@login_required
def accommodation():
	form = AccommodationForm()
	if form.validate_on_submit():
		accommodationData = Accommodation(
			name = form.name.data,
			address = form.address.data,
			arr_date = form.arr_date.data,
			in_time = form.in_time.data,
			out_date = form.out_date.data,
			out_time = form.out_time.data,
			comments = form.comments.data,
			author = current_user
		)
		db.session.add(accommodationData)
		db.session.commit()
		return redirect(url_for('activities'))
		return render_template('accommodation.html', title='accommodation', form=form, accommodation=accommodationData)
	else:
		print(form.errors)
		return render_template('accommodation.html', title='accommodation', form=form)

@app.route('/activities', methods=['GET','POST'])
@login_required
def activities():
	form = ActivitiesForm()
	if form.validate_on_submit():
		activitiesData = Activities(
			name = form.name.data,
			location = form.location.data,
			date = form.date.data,
			start = form.start.data,
			end = form.end.data,
			comments = form.comments.data,
			author = current_user
		)
		db.session.add(activitiesData)
		db.session.commit()
		return redirect(url_for('home'))
		if form.another.data:
			return redirect(url_for('activities'))
	elif form.cancel.data:
		return redirect(url_for('home'))
		return render_template('activities.html', title='activities', form=form, activities=activitiesData)
	else:
		print(form.errors)
		return render_template('activities.html', title='activities', form=form)


@app.route('/trip')
def trip():
	postData = Posts.query.all()
	flightData = Flights.query.all()
	accommodationData = Accommodation.query.all()
	activitiesData = Activities.query.all()
	return render_template('trip.html', title='your trip', posts=postData, flights=flightData, activities=activitiesData)

def holiday():
	holidays = []
	posts = Posts.query.filter_by(author=current_user)
	for post in posts:
		holidays.append(post)
	return holidays

#oliday123=holiday()