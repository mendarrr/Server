import pytest
from app import app, db
from models import User, Admin, Meal, Order, Category
from flask_jwt_extended import create_access_token
import json

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_register_user(test_client):
    response = test_client.post('/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'role': 'user'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_register_admin_not_allowed(test_client):
    response = test_client.post('/register', json={
        'username': 'testadmin',
        'email': 'testadmin@example.com',
        'password': 'password123',
        'role': 'admin'
    })
    assert response.status_code == 403
    assert b'Admin registration is not allowed via this route' in response.data

def test_login_user(test_client):
    response = test_client.post('/login', json={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data

def test_login_invalid_credentials(test_client):
    response = test_client.post('/login', json={
        'email': 'nonexistent@example.com',
        'password': 'password123'
    })
    assert response.status_code == 401
    assert b'Invalid email or password' in response.data

def test_get_users(test_client):
    response = test_client.get('/users')
    assert response.status_code == 200
    users = json.loads(response.data)
    assert len(users) > 0

def test_get_user_by_id(test_client):
    response = test_client.get('/users/1')
    assert response.status_code == 200
    user = json.loads(response.data)
    assert user['username'] == 'testuser'

def test_add_user(test_client):
    response = test_client.post('/users', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'role': 'user'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_update_user(test_client):
    response = test_client.put('/users/1', json={
        'username': 'updateduser'
    })
    assert response.status_code == 200
    assert b'User updated successfully' in response.data

def test_delete_user(test_client):
    response = test_client.delete('/users/1')
    assert response.status_code == 200
    assert b'User deleted successfully' in response.data

def test_add_admin(test_client):
    token = create_access_token(identity={'id': 1, 'role': 'admin'})
    headers = {'Authorization': f'Bearer {token}'}
    
    response = test_client.post('/admin_register', json={
        'username': 'testadmin',
        'email': 'testadmin@example.com',
        'password': 'password123'
    }, headers=headers)
    assert response.status_code == 201
    assert b'Admin created successfully' in response.data

def test_get_admins(test_client):
    response = test_client.get('/admins')
    assert response.status_code == 200
    admins = json.loads(response.data)
    assert len(admins) > 0

def test_add_meal(test_client):
    token = create_access_token(identity={'id': 1, 'role': 'admin'})
    headers = {'Authorization': f'Bearer {token}'}
    response= test_client.post('/meals', json={
        'meal_name': 'Test Meal',
        'price': 10.99,
        'category_id': 1,
        'image': 'test_image.jpg'
    })

def test_get_meals(test_client):
    response = test_client.get('/meals')
    assert response.status_code == 200
    meals = json.loads(response.data)
    assert len(meals) >= 0

def test_add_order(test_client):
    token = create_access_token(identity={'id': 1, 'role': 'user'})
    headers = {'Authorization': f'Bearer {token}'}

    response = test_client.post('/orders', json={
        'meal_id': 1
    }, headers=headers)
    assert response.status_code == 201
    assert b'Order placed successfully' in response.data

def test_get_orders(test_client):
    response = test_client.get('/orders')
    assert response.status_code == 200
    orders = json.loads(response.data)
    assert len(orders) >= 0

def test_add_category(test_client):
    response = test_client.post('/categories', json={
        'category_name': 'Test Category'
    })
    assert response.status_code == 201
    assert b'Category added successfully' in response.data

def test_get_categories(test_client):
    response = test_client.get('/categories')
    assert response.status_code == 200
    categories = json.loads(response.data)
    assert len(categories) > 0
