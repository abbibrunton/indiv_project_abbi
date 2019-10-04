from application import db, login_manager
from flask_login import UserMixin #is_authenticated, is_active, is_anonymous, get_id

@login_manager.user_loader #gets id from session
def load_user(id):
	return Users.query.get(int(id))



class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30), nullable=False)
	last_name = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(150), nullable=False, unique=True)
	password = db.Column(db.String(50), nullable=False)
	posts = db.relationship('Posts', backref='author', lazy=True)
	flights = db.relationship('Flights', backref='author', lazy=True)
	accommodation = db.relationship('Accommodation', backref='author', lazy=True)
	activities = db.relationship('Activities', backref='author', lazy=True)
	def __repr__(self):
		return ''.join(['user id: ', str(self.id), '\r\n', 'email: ', self.email, '\r\n', 'name: ', self.first_name, ' ', self.last_name])

class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False, unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #foreign key links data between tables
	def __repr__(self):
		return ''.join(['user id: ', str(self.user_id), '\r\n', 'name: ', self.name])

class Flights(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	holiday1 = db.Column(db.Integer, nullable=False)
	date1 = db.Column(db.String(50), nullable=False)
	depart = db.Column(db.String(50), nullable=False)
	time_d = db.Column(db.String(50), nullable=False)
	arrive = db.Column(db.String(50), nullable=False)
	time_a = db.Column(db.String(50), nullable=False)
	time_a_l = db.Column(db.String(50), nullable=False)
	date2 = db.Column(db.String(50), nullable=False)
	depart1 = db.Column(db.String(50), nullable=False)
	time_d1 = db.Column(db.String(50), nullable=False)
	arrive1 = db.Column(db.String(50), nullable=False)
	time_a1 = db.Column(db.String(50), nullable=False)
	time_a_l1 = db.Column(db.String(50), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #foreign key links data between tables

	def __repr__(self):
		return ''.join(['user id: ', self.user_id, '\r\n', 'depature airport: ', self.depart, '\r\n', 'departure time: ', self.time_d, '\r\n', 'arrival airport: ', self.arrive, '\r\n', 'arrival time: ', self.time_a, '\r\n', 'arrival time (local): ', self.time_a_l, 'r\n', 'holiday: ', self.holiday1])

class Accommodation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	address = db.Column(db.String(50), nullable=False)
	arr_date = db.Column(db.String(50), nullable=False)
	in_time = db.Column(db.String(50), nullable=True)
	out_date = db.Column(db.String(50), nullable=False)
	out_time = db.Column(db.String(50), nullable=True)
	comments = db.Column(db.String(100), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	def __repr__(self):
		return ''.join(['user id: ', self.user_id, '\r\n', 'accommodation name: ', self.name, '\r\n', 'arrival date: ', self.arr_date, '\r\n', 'check-in time: ', self.in_time, '\r\n', 'leaving date: ', self.out_time, '\r\n', 'check-out time: ', self.out_time, '\r\n', 'other info: ', self.comments])

class Activities(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	location = db.Column(db.String(50), nullable=False)
	date = db.Column(db.String(50), nullable=False)
	start = db.Column(db.String(50), nullable=True)
	end = db.Column(db.String(50), nullable=True)
	comments = db.Column(db.String(100), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	def __repr__(self):
		return ''.join(['user id: ', self.user_id, '\r\n', 'activity name: ', self.name, '\r\n', 'date: ', self.date, '\r\n', 'start time: ', self.start, '\r\n', 'end time: ', self.end, '\r\n', 'other info: ', self.comments])



