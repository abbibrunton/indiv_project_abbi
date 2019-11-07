
from application import db
from application.models import Users, Posts, Flights, Accommodation, Activities
db.drop_all()
db.create_all()
