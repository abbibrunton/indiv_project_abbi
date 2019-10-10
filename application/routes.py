from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Posts, Users, Flights, Accommodation, Activities
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm, FlightForm, AccommodationForm, ActivitiesForm
from flask_login import login_user, current_user, logout_user, login_required
# login user makes and maintains a session for the logged in user
# current user checks if authenticated - authenticated, active, can get id
# logout user removes the user session from being logged in
# login required forces user to be logged in

cycle = []

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

		return redirect(url_for('flights'))
		#return render_template('post.html', title='post', form=form, posts=alltheposts)
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
		posts = Posts.query.filter_by(user_id=current_user.id).all()
		flights = Flights.query.filter_by(user_id=current_user.id).all()
		accommodation = Accommodation.query.filter_by(user_id=current_user.id).all()
		activities = Activities.query.filter_by(user_id=current_user.id).all()
		for i in posts:
			db.session.delete(i)
		for i in flights:
			db.session.delete(i)
		for i in accommodation:
			db.session.delete(i)
		for i in activities:
			db.session.delete(i)
		db.session.delete(current_user)
		db.session.commit()
		logout_user()
		return redirect(url_for('register'))
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
	form = FlightForm()
	cycle = []
	for field in form:
		if field.type == 'SelectField':
			field.choices = cycle
	for post in Posts.query.all():
		if post.user_id == current_user.id:
			cycle.append((post.name, post.name))
	form.holiday1.choices = cycle
	
	if form.validate_on_submit():
		flightData = Flights(
			holiday1 = str(form.holiday1.data),
			date1 = str(form.date1.data),
			depart = str(form.depart.data),
			time_d = str(form.time_d.data),
			arrive = str(form.arrive.data),
			time_a = str(form.time_a.data),
			time_a_l = str(form.time_a_l.data),
			date2 = str(form.date2.data),
			depart1 = str(form.depart1.data),
			time_d1 = str(form.time_d1.data),
			arrive1 = str(form.arrive1.data),
			time_a1 = str(form.time_a1.data),
			time_a_l1 = str(form.time_a_l1.data),
			author = current_user
		)
		db.session.add(flightData)
		db.session.commit()
		return redirect(url_for('accommodation'))
	else:
		return render_template('flights.html', title='flights', form=form)

@app.route('/accommodation', methods=['GET','POST'])
@login_required
def accommodation():
	form = AccommodationForm()
	cycle = []
	for field in form:
		if field.type == 'SelectField':
			field.choices = cycle
	for post in Posts.query.all():
		if post.user_id == current_user.id:
			cycle.append((post.name, post.name))
	form.holiday1.choices = cycle

	if form.validate_on_submit():
		accommodationData = Accommodation(
			holiday1 = str(form.holiday1.data),
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
	else:
		print(form.errors)
		return render_template('accommodation.html', title='accommodation', form=form)

@app.route('/activities', methods=['GET','POST'])
@login_required
def activities():
	form = ActivitiesForm()
	cycle = []
	for field in form:
		if field.type == 'SelectField':
			field.choices = cycle
	for post in Posts.query.all():
		if post.user_id == current_user.id:
			cycle.append((post.name, post.name))
	form.holiday1.choices = cycle

	if form.validate_on_submit():
		activitiesData = Activities(
			holiday1 = str(form.holiday1.data),
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
		if form.another.data:
			return redirect(url_for('activities'))
		else:
			return redirect(url_for('home'))
	elif form.cancel.data:
		return redirect(url_for('home'))
	else:
		print(form.errors)
		return render_template('activities.html', title='activities', form=form)


@app.route('/trip', methods=['GET','POST'])
def trip():
	postData = Posts.query.filter_by(user_id=current_user.id).all()
	flightData = Flights.query.all()
	accommodationData = Accommodation.query.all()
	activitiesData = Activities.query.all()


	return render_template('trip.html', title='your trip', posts=postData, flights=flightData, activities=activitiesData, accommodation=accommodationData)

@app.route('/edit', methods=['GET','POST'])
def edit():
	flightData = Flights.query.all()
	posts=Posts.query.filter_by(user_id=current_user.id).all()
	return render_template('edit.html', title='edit', posts=posts, flights=flightData)

@app.route('/edittrip/<int(min=1):trip_id>', methods=['GET','POST'])
def edittrip(trip_id):
	#delete(trip_id)
	posts=Posts.query.filter_by(id=trip_id).first()
	flights=Flights.query.filter_by(holiday1=posts.name).first()
	return render_template('edittrip.html', title='edit trip', trip_id=trip_id, posts=posts, flights=flights)

