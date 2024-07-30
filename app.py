from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import create_app, db
from models import User, Admin, Meal, Order, Category
from datetime import datetime

app = create_app()
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

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

# CRUD for Users
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    } for user in users])

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })

@app.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# CRUD for Admins
@app.route('/admins', methods=['GET'])
@jwt_required()
def get_admins():
    admins = Admin.query.all()
    return jsonify([{
        'id': admin.id,
        'username': admin.username,
        'email': admin.email
    } for admin in admins])

@app.route('/admins/<int:id>', methods=['GET'])
@jwt_required()
def get_admin(id):
    admin = Admin.query.get_or_404(id)
    return jsonify({
        'id': admin.id,
        'username': admin.username,
        'email': admin.email
    })

@app.route('/admins/<int:id>', methods=['PUT'])
@jwt_required()
def update_admin(id):
    data = request.get_json()
    admin = Admin.query.get_or_404(id)
    if 'username' in data:
        admin.username = data['username']
    if 'email' in data:
        admin.email = data['email']
    db.session.commit()
    return jsonify({'message': 'Admin updated successfully'})

@app.route('/admins/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_admin(id):
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'message': 'Admin deleted successfully'})

# CRUD for Meals
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

@app.route('/meals/<int:id>', methods=['GET'])
@jwt_required()
def get_meal(id):
    meal = Meal.query.get_or_404(id)
    return jsonify({
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'price': meal.price
    })

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

# CRUD for Categories
@app.route('/categories', methods=['POST'])
@jwt_required()
def add_category():
    data = request.get_json()
    if not all(k in data for k in ('category_name', 'image')):
        return jsonify({'message': 'Missing category name or image'}), 400

    category = Category(
        category_name=data['category_name'],
        image=data['image']
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully'}), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': category.id,
        'category_name': category.category_name,
        'image': category.image
    } for category in categories])

@app.route('/categories/<int:id>', methods=['GET'])
@jwt_required()
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify({
        'id': category.id,
        'category_name': category.category_name,
        'image': category.image
    })

@app.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    data = request.get_json()
    category = Category.query.get_or_404(id)
    if 'category_name' in data:
        category.category_name = data['category_name']
    if 'image' in data:
        category.image = data['image']
    db.session.commit()
    return jsonify({'message': 'Category updated successfully'})

@app.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})

# CRUD for Orders
@app.route('/orders', methods=['POST'])
@jwt_required()
def place_order():
    data = request.get_json()
    if not all(k in data for k in ('meal_id',)):
        return jsonify({'message': 'Missing meal_id'}), 400

    user_id = get_jwt_identity()
    meal = Meal.query.get_or_404(data['meal_id'])
    order = Order(
        user_id=user_id,
        meal_id=meal.id
    )
    db.session.add(order)
    db.session.commit()

    # Decrease user balance and increase admin balance logic
    return jsonify({'message': 'Order placed successfully'}), 201

@app.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'user_id': order.user_id,
        'meal_id': order.meal_id,
        'order_time': order.order_time
    } for order in orders])

@app.route('/orders/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        'id': order.id,
        'user_id': order.user_id,
        'meal_id': order.meal_id,
        'order_time': order.order_time
    })

@app.route('/orders/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
