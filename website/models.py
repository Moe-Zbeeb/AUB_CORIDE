from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from flask_login import login_user, login_required, logout_user, current_user
# Association table for Many-to-Many relationship between users and carpools
user_carpools = db.Table('user_carpools',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('carpool_id', db.Integer, db.ForeignKey('carpool.id'), primary_key=True)
)

class Carpool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)  
    from_location = db.Column(db.String(255), nullable=False)
    to_location = db.Column(db.String(255), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=func.now())
    passengers = db.relationship('User', secondary=user_carpools, back_populates='carpools')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Reference to the User who owns the carpool

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150))
    gender = db.Column(db.String(10))    
    points = db.Column(db.Integer , default=0)
    carpools = db.relationship('Carpool', secondary=user_carpools, back_populates='passengers')
