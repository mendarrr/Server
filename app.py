from models import User, Admin, Category, Meals, Transactions
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime, timedelta
from config import DevelopmentConfig, ProductionConfig , db

app = Flask(_name_)
CORS(app)

# Routes
@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def post(self):
        data = request.get_json()
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            role=data.get('role')
        )
        user.set_password(data.get('password'))
        try:
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.role = data.get('role', user.role)
            if data.get('password'):
                user.set_password(data.get('password'))
            try:
                db.session.commit()
                return user.to_dict(), 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return {'message': 'User deleted'}, 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'User not found'}, 404

class AdminResource(Resource):
    def get(self, admin_id=None):
        if admin_id:
            admin = Admin.query.get(admin_id)
            if admin:
                return admin.to_dict(), 200
            return {'error': 'Admin not found'}, 404
        admins = Admin.query.all()
        return [admin.to_dict() for admin in admins], 200

    def post(self):
        data = request.get_json()
        admin = Admin(
            user_id=data.get('user_id')
        )
        try:
            db.session.add(admin)
            db.session.commit()
            return admin.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    def put(self, admin_id):
        data = request.get_json()
        admin = Admin.query.get(admin_id)
        if admin:
            admin.user_id = data.get('user_id', admin.user_id)
            try:
                db.session.commit()
                return admin.to_dict(), 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'Admin not found'}, 404

    def delete(self, admin_id):
        admin = Admin.query.get(admin_id)
        if admin:
            try:
                db.session.delete(admin)
                db.session.commit()
                return {'message': 'Admin deleted'}, 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'Admin not found'}, 404

class MealsResource(Resource):
    def get(self, meal_id=None):
        if meal_id:
            meal = Meals.query.get(meal_id)
            if meal:
                return meal.to_dict(), 200
            return {'error': 'Meal not found'}, 404
        meals = Meals.query.all()
        return [meal.to_dict() for meal in meals], 200

    def post(self):
        data = request.get_json()
        meal = Meals(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            admin_id=data.get('admin_id')
        )
        try:
            db.session.add(meal)
            db.session.commit()
            return meal.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    def put(self, meal_id):
        data = request.get_json()
        meal = Meals.query.get(meal_id)
        if meal:
            meal.name = data.get('name', meal.name)
            meal.description = data.get('description', meal.description)
            meal.price = data.get('price', meal.price)
            meal.admin_id = data.get('admin_id', meal.admin_id)
            try:
                db.session.commit()
                return meal.to_dict(), 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'Meal not found'}, 404

    def delete(self, meal_id):
        meal = Meals.query.get(meal_id)
        if meal:
            try:
                db.session.delete(meal)
                db.session.commit()
                return {'message': 'Meal deleted'}, 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'Meal not found'}, 404

class TransactionsResource(Resource):
    def get(self, transaction_id=None):
        if transaction_id:
            transaction = Transactions.query.get(transaction_id)
            if transaction:
                return transaction.to_dict(), 200
            return {'error': 'Transaction not found'}, 404
        transactions = Transactions.query.all()
        return [transaction.to_dict() for transaction in transactions], 200

    def post(self):
        data = request.get_json()
        transaction = Transactions(
            user_id=data.get('user_id'),
            meal_id=data.get('meal_id')
        )
        try:
            db.session.add(transaction)
            db.session.commit()
            return transaction.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    def put(self, transaction_id):
        data = request.get_json()
        transaction = Transactions.query.get(transaction_id)
        if transaction:
            transaction.user_id = data.get('user_id', transaction.user_id)
            transaction.meal_id = data.get('meal_id', transaction.meal_id)
            try:
                db.session.commit()
                return transaction.to_dict(), 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'Transaction not found'}, 404

    def delete(self, transaction_id):
        transaction = Transactions.query.get(transaction_id)
        if transaction:
            try:
                db.session.delete(transaction)
                db.session.commit()
                return {'message': 'Transaction deleted'}, 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'Transaction not found'}, 404

class CategoryResource(Resource):
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get(category_id)
            if category:
                return category.to_dict(), 200
            return {'error': 'Category not found'}, 404
        categories = Category.query.all()
        return [category.to_dict() for category in categories], 200

    def post(self):
        data = request.get_json()
        category = Category(
            category_name=data.get('category_name'),
            image=data.get('image')
        )
        try:
            db.session.add(category)
            db.session.commit()
            return category.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    def put(self, category_id):
        data = request.get_json()
        category = Category.query.get(category_id)
        if category:
            category.category_name = data.get('category_name', category.category_name)
            category.image = data.get('image', category.image)
            try:
                db.session.commit()
                return category.to_dict(), 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'Category not found'}, 404

    def delete(self, category_id):
        category = Category.query.get(category_id)
        if category:
            try:
                db.session.delete(category)
                db.session.commit()
                return {'message': 'Category deleted'}, 200
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        return {'error': 'Category not found'}, 404

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(AdminResource, '/admins', '/admins/<int:admin_id>')
api.add_resource(MealsResource, '/meals', '/meals/<int:meal_id>')
api.add_resource(TransactionsResource, '/transactions', '/transactions/<int:transaction_id>')
api.add_resource(CategoryResource, '/categories', '/categories/<int:category_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)