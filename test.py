from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users, Posts
from application import bcrypt
from flask_login import current_user

id = db.Column(db.Integer, primary_key=True)
print(id)
#cycle = []
lists = Posts.query.filter_by(user_id=current_user.id).all()
#	for i in range(int(len(lists))):#
#		temp = [lists[i], lists[i]]
#		cycle.append(temp)