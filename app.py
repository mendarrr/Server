from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime
from config import create_app, db
from models import User, Admin, Meal, Offer,Order, Category , Transaction

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

@app.route('/admin_register', methods=['POST'])
@jwt_required()
def admin_register():
    admin_count = Admin.query.count()
    if admin_count >= 5:
        return jsonify({'message': 'Cannot add more than 5 admins'}), 403

    data = request.get_json()
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    admin = Admin(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )

    db.session.add(admin)
    db.session.commit()
    return jsonify({'message': 'Admin created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()
    admin = Admin.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': 'user'})
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'role': 'user'
        }), 200

    elif admin and bcrypt.check_password_hash(admin.password_hash, data['password']):
        access_token = create_access_token(identity={'id': admin.id, 'role': 'admin'})
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
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    } for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })

@app.route('/users', methods=['POST'])
def add_user():
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

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    if 'role' in data:
        user.role = data['role']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# CRUD for Admins
@app.route('/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([{
        'id': admin.id,
        'username': admin.username,
        'email': admin.email
    } for admin in admins])

@app.route('/admins/<int:id>', methods=['GET'])
def get_admin(id):
    admin = Admin.query.get_or_404(id)
    return jsonify({
        'id': admin.id,
        'username': admin.username,
        'email': admin.email
    })

@app.route('/admins', methods=['POST'])
def add_admin():
    admin_count = Admin.query.count()
    if admin_count >= 5:
        return jsonify({'message': 'Cannot add more than 5 admins'}), 403

    data = request.get_json()
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    admin = Admin(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )

    db.session.add(admin)
    db.session.commit()
    return jsonify({'message': 'Admin created successfully'}), 201

@app.route('/admins/<int:id>', methods=['PUT'])
def update_admin(id):
    data = request.get_json()
    admin = Admin.query.get_or_404(id)
    if 'username' in data:
        admin.username = data['username']
    if 'email' in data:
        admin.email = data['email']
    if 'password' in data:
        admin.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    db.session.commit()
    return jsonify({'message': 'Admin updated successfully'})

@app.route('/admins/<int:id>', methods=['DELETE'])
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
    if not all(k in data for k in ('name', 'price', 'category_id', 'image')):
        return jsonify({'message': 'Missing meal name, price, category_id, or image'}), 400

    admin_id = get_jwt_identity()
    meal = Meal(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        image=data['image'],
        category_id=data['category_id'],
        admin_id=admin_id['id']
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
        'price': meal.price,
        'image': meal.image,
        'category': meal.category.category_name
    } for meal in meals])

@app.route('/meals/<int:id>', methods=['GET'])
def get_meal(id):
    meal = Meal.query.get_or_404(id)
    return jsonify({
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'price': meal.price,
        'image': meal.image,
        'category': meal.category.category_name
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
    if 'image' in data:
        meal.image = data['image']
    if 'category_id' in data:
        meal.category_id = data['category_id']
    db.session.commit()
    return jsonify({'message': 'Meal updated successfully'})

@app.route('/meals/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_meal(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    return jsonify({'message': 'Meal deleted successfully'})

# CRUD for Orders
@app.route('/orders', methods=['POST'])
@jwt_required()
def add_order():
    data = request.get_json()
    current_user = get_jwt_identity()

    if 'meal_id' not in data:
        return jsonify({'message': 'Missing meal ID'}), 400

    order = Order(
        user_id=current_user['id'],
        meal_id=data['meal_id']
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'user': order.user.username,
        'meal': order.meal.name,
        'order_time': order.order_time
    } for order in orders])

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        'id': order.id,
        'user': order.user.username,
        'meal': order.meal.name,
        'order_time': order.order_time
    })

# CRUD for Categories
@app.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    if 'category_name' not in data:
        return jsonify({'message': 'Missing category name'}), 400

    # Create a new category with description
    category = Category(
        category_name=data['category_name'],
        description=data.get('description'),  # Add this line
        image=data.get('image')
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
        'description': category.description,  # Add this line
        'image': category.image
    } for category in categories])

@app.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify({
        'id': category.id,
        'category_name': category.category_name,
        'description': category.description,  # Add this line
        'image': category.image
    })

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    category = Category.query.get_or_404(id)
    if 'category_name' in data:
        category.category_name = data['category_name']
    if 'description' in data:
        category.description = data['description']  # Add this line
    if 'image' in data:
        category.image = data['image']
    db.session.commit()
    return jsonify({'message': 'Category updated successfully'})

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})

@app.route("/categories/<int:id>/meals", methods=["GET"])
def get_meals_by_category(id):
    category = Category.query.get_or_404(id)
    meals = category.meals
    return jsonify([{
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'price': meal.price,
        'image': meal.image,
        'category': meal.category.category_name
    } for meal in meals])
@app.route('/offers', methods=['POST'])
@jwt_required()
def create_offer():
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'message': 'Admin privileges required'}), 403

    data = request.json
    offer_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    meal_ids = data['meals']
    for meal_id in meal_ids:
        new_offer = Offer(offer_date=offer_date, meal_id=meal_id)
        db.session.add(new_offer)
    db.session.commit()
    return jsonify({'message': 'Offers created successfully'}), 201

@app.route('/offers', methods=['GET'])
def get_offers():
    offers = db.session.query(Offer).all()
    offers_data = {}
    for offer in offers:
        date_str = offer.offer_date.strftime('%Y-%m-%d')
        if date_str not in offers_data:
            offers_data[date_str] = []
        meal = db.session.query(Meal).get(offer.meal_id)
        if meal is None:
            continue  
        meal_data = {
            'id': offer.id,  
            'name': meal.name,
            'image': meal.image,
            'price': meal.price,
            'description': meal.description
        }
        offers_data[date_str].append(meal_data)
    return jsonify(offers_data), 200

@app.route('/offers/<int:id>', methods=['PUT'])
@jwt_required()
def update_offer(id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'message': 'Admin privileges required'}), 403

    offer = Offer.query.get_or_404(id)
    data = request.get_json()
    
    # Update offer date
    if 'date' in data:
        try:
            offer_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            offer.offer_date = offer_date
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Update meal details 
    if 'meal' in data:
        meal = Meal.query.get_or_404(offer.meal_id)
        
        if 'name' in data['meal']:
            meal.name = data['meal']['name']
        
        if 'description' in data['meal']:
            meal.description = data['meal']['description']
        
        if 'price' in data['meal']:
            try:
                meal.price = float(data['meal']['price'])
            except ValueError:
                return jsonify({'message': 'Invalid price format'}), 400
    
    db.session.commit()
    return jsonify({'message': 'Offer updated successfully'}), 200

@app.route('/offers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_offer(id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'message': 'Admin privileges required'}), 403

    offer = Offer.query.get_or_404(id)
    db.session.delete(offer)
    db.session.commit()
    return jsonify({'message': 'Offer deleted successfully'}), 200

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    current_user = get_jwt_identity()

    # Check if the current user has admin privileges
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Admin privileges required'}), 403

    # Fetch all transactions from the database
    transactions = Transaction.query.all()
    transactions_list = [{
        'id': transaction.id,
        'userName': transaction.user.username,  
        'date': transaction.transaction_date.strftime('%Y-%m-%d'),  
        'items': transaction.items.split(','),  
        'total': transaction.total
    } for transaction in transactions]

    return jsonify(transactions_list), 200


@app.route('/transactions', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()

        user = User.query.filter_by(username=data['userName']).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_transaction = Transaction(
            user_id=user.id,
            total=data['total'],
            items=','.join(data['items']),
            transaction_date=datetime.strptime(data['date'], '%Y-%m-%d')
        )

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({"message": "Transaction created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

