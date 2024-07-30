from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import create_app, db
from models import User, Admin, Meal, Transaction, Category
from datetime import datetime

app = create_app()

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User Management
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(k in data for k in ('username', 'email', 'password', 'role')):
        return jsonify({'message': 'Missing required fields'}), 400

    if data['role'] == 'admin':
        return jsonify({'message': 'Admin registration is not allowed via this route'}), 403

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
    admin = Admin.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'role': user.role
        }), 200

    elif admin and bcrypt.check_password_hash(admin.password_hash, data['password']):
        access_token = create_access_token(identity=admin.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'role': 'admin'
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

@app.route('/meals/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_meal(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    return jsonify({'message': 'Meal deleted successfully'})

# Menu Setup
@app.route('/menu', methods=['POST'])
@jwt_required()
def setup_menu():
    data = request.get_json()
    # Assume menu setup logic
    return jsonify({'message': 'Menu setup successful'}), 201

@app.route('/menu/<string:date>', methods=['GET'])
def get_menu(date):
    # Assume menu retrieval logic
    return jsonify({'message': 'Menu retrieved successfully'})

# Order Management
@app.route('/orders', methods=['POST'])
@jwt_required()
def place_order():
    data = request.get_json()
    if 'meal_id' not in data:
        return jsonify({'message': 'Missing meal_id'}), 400

    transaction = Transaction(
        user_id=get_jwt_identity(),
        meal_id=data['meal_id']
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'}), 201

@app.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': order.id,
        'meal_id': order.meal_id,
        'timestamp': order.timestamp.isoformat()
    } for order in orders])

@app.route('/orders/admin', methods=['GET'])
@jwt_required()
def get_orders_admin():
    orders = Transaction.query.all()
    return jsonify([{
        'id': order.id,
        'user_id': order.user_id,
        'meal_id': order.meal_id,
        'timestamp': order.timestamp.isoformat()
    } for order in orders])

@app.route('/revenue', methods=['GET'])
@jwt_required()
def get_revenue():
    # Assume revenue calculation logic
    return jsonify({'revenue': 1000.00})

# Admin Management Routes
@app.route('/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([{
        'id': admin.id,
        'username': admin.username,
        'email': admin.email
    } for admin in admins])

@app.route('/admin', methods=['POST'])
def add_admin():
    data = request.get_json()
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    existing_admins = Admin.query.all()
    if len(existing_admins) >= 5:
        return jsonify({'message': 'Cannot add more than 5 admins'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    admin = Admin(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )
    db.session.add(admin)
    db.session.commit()
    return jsonify({'message': 'Admin created successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
