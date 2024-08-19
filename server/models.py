# models.py

from config import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Admin {self.username}>'

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(300), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # Foreign key to Category
    admin = db.relationship('Admin', backref=db.backref('meals', lazy=True))
    category = db.relationship('Category', backref=db.backref('meals', lazy=True))  # Relationship to Category

    def __repr__(self):
        return f'<Meal {self.name}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String)
    image = db.Column(db.String)

    def __repr__(self):
        return f'<Category {self.category_name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    meal = db.relationship('Meal', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'<Order {self.id}>'
class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offer_date = db.Column(db.Date, nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    meal = db.relationship('Meal', backref=db.backref('offers', lazy=True))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    items = db.Column(db.String(500), nullable=False) 
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f'<Transaction {self.id} - User {self.user_id}>'