from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.column(db.String(20), nullable=False) # role 'client' or 'admin'
    transactions = db.relationship('Transactions', pack_populates='User', lazy='True')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Admin(db.Model):
    __tablename__ = 'Admin'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', pack_populates=db.backref('Admin', uselist=False))
    meals = db.relationship('Meals', pack_populates='Admin', lazy=True)

class Meals(db.Model):
    __tablename__ ='Meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    transactions = db.relationship('Transactions', back_populates='Meals', lazy=True)

class Transactions(db.Model):
    __tablename__ = 'Transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime)

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    Category_name = db.Column(db.String(80), unique=True, nullable=False)
    image = db.Column(db.String, nullable=False)
    meal_id = db.relationship('Meals', back_populates='Category')