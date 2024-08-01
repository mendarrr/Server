import pytest
from app import create_app, db
from models import User, Admin, Meal, Category, Order

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_model(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com', password_hash='hashedpassword', role='user')
        db.session.add(user)
        db.session.commit()
        assert User.query.filter_by(email='test@example.com').first() is not None

def test_admin_model(app):
    with app.app_context():
        admin = Admin(username='testadmin', email='admin@example.com', password_hash='hashedpassword')
        db.session.add(admin)
        db.session.commit()
        assert Admin.query.filter_by(email='admin@example.com').first() is not None

def test_meal_model(app):
    with app.app_context():
        category = Category(category_name='Test Category')
        admin = Admin(username='testadmin', email='admin@example.com', password_hash='hashedpassword')
        db.session.add(category)
        db.session.add(admin)
        db.session.commit()

        meal = Meal(name='Test Meal', description='Test Description', price=10.99, image='test.jpg', admin_id=admin.id, category_id=category.id)
        db.session.add(meal)
        db.session.commit()
        assert Meal.query.filter_by(name='Test Meal').first() is not None

def test_category_model(app):
    with app.app_context():
        category = Category(category_name='Test Category', image='category.jpg')
        db.session.add(category)
        db.session.commit()
        assert Category.query.filter_by(category_name='Test Category').first() is not None

def test_order_model(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com', password_hash='hashedpassword', role='user')
        category = Category(category_name='Test Category')
        admin = Admin(username='testadmin', email='admin@example.com', password_hash='hashedpassword')
        db.session.add_all([user, category, admin])
        db.session.commit()

        meal = Meal(name='Test Meal', description='Test Description', price=10.99, image='test.jpg', admin_id=admin.id, category_id=category.id)
        db.session.add(meal)
        db.session.commit()

        order = Order(user_id=user.id, meal_id=meal.id)
        db.session.add(order)
        db.session.commit()
        assert Order.query.filter_by(user_id=user.id, meal_id=meal.id).first() is not None