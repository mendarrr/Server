from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import create_app, db
from models import User, Admin, Meal, Transaction, Category
from datetime import datetime

app = create_app()

bcrypt = Bcrypt()
jwt = JWTManager(app)

# User Management
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(k in data for k in ('username', 'email', 'password', 'role')):
        return jsonify({'message': 'Missing required fields'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'role': user.role
        }), 200
    return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logout successful'})

# Meal Management
@app.route('/meals', methods=['POST'])
@jwt_required()
def add_meal():
    data = request.get_json()
    if not all(k in data for k in ('name', 'price')):
        return jsonify({'message': 'Missing meal name or price'}), 400

    admin_id = get_jwt_identity()
    meal = Meal(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        admin_id=admin_id
    )
    db.session.add(meal)
    db.session.commit()
    return jsonify({'message': 'Meal added successfully'}), 201

@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([{
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'price': meal.price
    } for meal in meals])

@app.route('/meals/<int:id>', methods=['PUT'])
@jwt_required()
def update_meal(id):
    data = request.get_json()
    meal = Meal.query.get_or_404(id)
    if 'name' in data:
        meal.name = data['name']
    if 'description' in data:
        meal.description = data['description']
    if 'price' in data:
        meal.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Meal updated successfully'})