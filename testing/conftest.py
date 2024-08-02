#!/usr/bin/env python3

import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db
from models import User, Admin, Category, Order

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def init_database(app):
    # Create test users
    user = User(username='testuser', email='test@example.com', password_hash='hashedpassword', role='user')
    admin = Admin(username='testadmin', email='admin@example.com', password_hash='hashedpassword')
    
    # Create test category
    category = Category(category_name='Test Category', image='category.jpg')
    order=Order(user_id=1, meal_id=1, order_time=1111)
    # Add to session and commit
    db.session.add_all([user, admin, category, order])
    db.session.commit()

    yield  # this is where the testing happens

    # Teardown
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='module')
def auth_tokens(client):
    # Get user token
    user_response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'hashedpassword'
    })
    user_token = user_response.json['access_token']

    # Get admin token
    admin_response = client.post('/login', json={
        'email': 'admin@example.com',
        'password': 'hashedpassword'
    })
    admin_token = admin_response.json['access_token']

    return {'user': user_token, 'admin': admin_token}