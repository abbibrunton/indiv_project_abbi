from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt, login_manager
from application.models import Posts, Users, Flights, Accommodation, Activities
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm, FlightForm, AccommodationForm, ActivitiesForm, EditForm
from flask_login import login_user, current_user, logout_user, login_required
# login user makes and maintains a session for the logged in user
# current user checks if authenticated - authenticated, active, can get id
# logout user removes the user session from being logged in
# login required forces user to be logged in

cycle = []
@login_manager.user_loader #gets id from session
def load_user(id):
	return Users.query.get(int(id))

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
	extra = ''
	for field in form:
		if field.type == 'SelectField':
			field.choices = cycle
	for post in Posts.query.all():
		if post.user_id == current_user.id:
			cycle.append((post.name, post.name))
	form.holiday1.choices = cycle
	
	if form.validate_on_submit():
		amount = Flights.query.filter_by(holiday1=str(form.holiday1.data)).all()
		if amount:
			amount = len(amount)
		else:
			amount = 0
		if amount < 1:
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
			extra = 'you can only have up to 1 flight per trip. please edit your existing flight or choose another trip.'
	else:
		print(form.errors)
	return render_template('flights.html', title='flights', form=form, more=extra)

@app.route('/accommodation', methods=['GET','POST'])
@login_required
def accommodation():
	form = AccommodationForm()
	cycle = []
	extra = ''
	for field in form:
		if field.type == 'SelectField':
			field.choices = cycle
	for post in Posts.query.all():
		if post.user_id == current_user.id:
			cycle.append((post.name, post.name))
	form.holiday1.choices = cycle

	if form.validate_on_submit():
		amount = Flights.query.filter_by(holiday1=str(form.holiday1.data)).all()
		if amount:
			amount = len(amount)
		else:
			amount = 0
		if amount < 1:
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
			extra = 'you can only have up to 1 accommodation per trip. please edit your existing accommodation or choose another trip.'
	else:
		print(form.errors)
	return render_template('accommodation.html', title='accommodation', form=form, more=extra)

@app.route('/activities', methods=['GET','POST'])
@login_required
def activities():
	form = ActivitiesForm()
	cycle = []
	extra = ''
	for field in form:
		if field.type == 'SelectField':
			field.choices = cycle
	for post in Posts.query.all():
		if post.user_id == current_user.id:
			cycle.append((post.name, post.name))
	form.holiday1.choices = cycle

	if form.validate_on_submit():
		amount = Activities.query.filter_by(holiday1=str(form.holiday1.data)).all()
		if amount:
			amount = len(amount)
		else:
			amount = 0
		if amount < 3:
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
			extra = 'you can only have up to 3 activities per trip. please delete one and try again.'
	else:
		print(form.errors)
	return render_template('activities.html', title='activities', form=form, more=extra)

@app.route('/edit', methods=['GET','POST'])
def edit():
	flightData = Flights.query.all()
	posts=Posts.query.filter_by(user_id=current_user.id).all()
	return render_template('edit.html', title='edit', posts=posts, flights=flightData)

@app.route('/edittrip/<int(min=1):trip_id>', methods=['GET','POST'])
def edittrip(trip_id):
	form = EditForm()
	posts=Posts.query.filter_by(id=trip_id).first()
	flights=Flights.query.filter_by(holiday1=posts.name).first()
	accommodation=Accommodation.query.filter_by(holiday1=posts.name).first()
	activity=Activities.query.filter_by(holiday1=posts.name).all()
	activity_count=int(len(activity))
	if form.delete.data:
		db.session.delete(posts)
		db.session.delete(flights)
		db.session.delete(accommodation)
		for i in activity:
			db.session.delete(i)
		db.session.commit()
		return redirect(url_for('edit'))

	if form.is_submitted():
		if form.date1.data:
			flights.date1 = form.date1.data
		flights.depart = form.depart.data
		if form.time_d.data:
			flights.time_d = form.time_d.data
		flights.arrive = form.arrive.data
		if form.time_a.data:
			flights.time_a = form.time_a.data
		if form.time_a_l.data:
			flights.time_a_l = form.time_a_l.data
		if form.date2.data:
			flights.date2 = form.date2.data
		flights.depart1 = form.depart1.data
		if form.time_d1.data:
			flights.time_d1 = form.time_d1.data
		flights.arrive1 = form.arrive1.data
		if form.time_a1.data:
			flights.time_a1 = form.time_a1.data
		if form.time_a_l1.data:
			flights.time_a_l1 = form.time_a_l1.data

		accommodation.name = form.name.data
		accommodation.address = form.address.data
		if form.arr_date.data:
			accommodation.arr_date = form.arr_date.data
		if form.in_time.data:
			accommodation.in_time = form.in_time.data
		if form.out_date.data:
			accommodation.out_date = form.out_date.data
		if form.out_time.data:
			accommodation.out_time = form.out_time.data
		if accommodation.comments.data:
			accommodation.comments = form.comments.data
		i=1
		for j in activity:
			activity_id = j.id
			activities1=Activities.query.filter_by(id=activity_id).first()
			if i == 1:
				activities1.name = form.a1_name1.data
				activities1.location = form.a1_location.data
				if form.a1_date.data:
					activities1.date = form.a1_date.data
				if form.a1_start.data:
					activities1.start = form.a1_start.data
				if form.a1_end.data:
					activities1.end = form.a1_end.data
				if activities1.comments.data:
					activities1.comments = form.a1_comments1.data

				if form.delete_a1.data:
					Activities.query.filter_by(id=activity_id).delete()

			elif i == 2:
				activities1.name = form.a2_name1.data
				activities1.location = form.a2_location.data
				if form.a2_date.data:
					activities1.date = form.a2_date.data
				if form.a2_start.data:
					activities1.start = form.a2_start.data
				if form.a2_end.data:
					activities1.end = form.a2_end.data
				if activities1.comments.data:
					activities1.comments = form.a2_comments1.data
				if form.delete_a2.data:
					Activities.query.filter_by(id=activity_id).delete()
			elif i == 3:
				activities1.name = form.a3_name1.data
				activities1.location = form.a3_location.data
				if form.a3_date.data:
					activities1.date = form.a3_date.data
				if form.a3_start.data:
					activities1.start = form.a3_start.data
				if form.a3_end.data:
					activities1.end = form.a3_end.data
				if activities1.comments.data:
					activities1.comments = form.a3_comments1.data
				if form.delete_a3.data:
					Activities.query.filter_by(id=activity_id).delete()
			i+=1

		db.session.commit()
		return redirect(url_for('edit'))

	elif request.method == 'GET':
		form.date1.data = flights.date1
		form.depart.data = flights.depart
		form.time_d.data = flights.time_d
		form.arrive.data = flights.arrive
		form.time_a.data = flights.time_a
		form.time_a_l.data = flights.time_a_l
		form.date2.data = flights.date2
		form.depart1.data = flights.depart1
		form.time_d1.data = flights.time_d1
		form.arrive1.data = flights.arrive1
		form.time_a1.data = flights.time_a1
		form.time_a_l1.data = flights.time_a_l1

		form.name.data = accommodation.name
		form.address.data = accommodation.address
		form.arr_date.data = accommodation.arr_date
		form.in_time.data = accommodation.in_time
		form.out_date.data = accommodation.out_date
		form.out_time.data = accommodation.out_time
		form.comments.data = accommodation.comments

		i=1
		for j in activity:
			activity_id = j.id
			activities1=Activities.query.filter_by(id=activity_id).first()
			if i == 1:
				form.a1_name1.data = activities1.name
				form.a1_location.data = activities1.location
				form.a1_date.data = activities1.date
				form.a1_start.data = activities1.start
				form.a1_end.data = activities1.end
				form.a1_comments1.data = activities1.comments
			elif i == 2:
				form.a2_name1.data = activities1.name
				form.a2_location.data = activities1.location
				form.a2_date.data = activities1.date
				form.a2_start.data = activities1.start
				form.a2_end.data = activities1.end
				form.a2_comments1.data = activities1.comments
			elif i == 3:
				form.a3_name1.data = activities1.name
				form.a3_location.data = activities1.location
				form.a3_date.data = activities1.date
				form.a3_start.data = activities1.start
				form.a3_end.data = activities1.end
				form.a3_comments1.data = activities1.comments
			i+=1

	return render_template('edittrip.html', title='edit trip', trip_id=trip_id, posts=posts, flights=flights, accommodation=accommodation, activities=activities, form=form, activity_count=activity_count)

@app.errorhandler(404)
def notfound_found(error):
	return render_template('error.html', title='error')


@app.route('/viewtrip/<int(min=1):trip_id>', methods=['GET'])
def viewtrip(trip_id):
	posts=Posts.query.filter_by(id=trip_id).first()
	flight=Flights.query.filter_by(holiday1=posts.name).first()
	accommodation=Accommodation.query.filter_by(holiday1=posts.name).first()
	activity=Activities.query.filter_by(holiday1=posts.name).all()


	return render_template('viewtrip.html', title='your trip', posts=posts, flight=flight, activities=activity, accommodation=accommodation)