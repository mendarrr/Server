from faker import Faker
from app import app
from models import User, Admin, Meal, Order, Category,db

if __name__ == '__main__':
    fake = Faker()

    with app.app_context():
        db.drop_all()
        db.create_all()

        users=[]
        for _ in range(10):
            user = User(
                username=fake.name(),
                email=fake.email(),
                password=fake.password(length=16),
                role="user"
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()

        print("Users added successfully")
        admins=[]
        for _ in range(5):
            admin = Admin(
                username=fake.name(),
                email=fake.email(),
                password_hash=fake.password(length=16)
            )
            admins.append(admin)
        db.session.add_all(admins)
        db.session.commit()

        print("Admins added successfully")
        
        
