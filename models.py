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
    role = db.Column(db.String(20), nullable=False)  # role 'client' or 'admin'
    transactions = db.relationship('Transaction', back_populates='user', lazy=True)
    admin = db.relationship('Admin', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Admin(db.Model):
    __tablename__ = 'Admin'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship('User', back_populates='admin')
    meals = db.relationship('Meal', back_populates='admin', lazy=True)

class Meal(db.Model):
    __tablename__ = 'Meal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.id'), nullable=False)
    admin = db.relationship('Admin', back_populates='meals')
    transactions = db.relationship('Transaction', back_populates='meal', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=True)
    category = db.relationship('Category', back_populates='meals')

class Transaction(db.Model):
    __tablename__ = 'Transaction'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('Meal.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='transactions')
    meal = db.relationship('Meal', back_populates='transactions')

class Category(db.Model):
    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(80), unique=True, nullable=False)
    image = db.Column(db.String, nullable=False)
    meals = db.relationship('Meal', back_populates='category')