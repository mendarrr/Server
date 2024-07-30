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
                password_hash=fake.password(length=16),
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
        
        categories=[
            Category(category_name="Appetizers", image="https://i.pinimg.com/236x/74/62/97/746297f074bed5db7f26cee0c1decc28.jpg"),
            Category(category_name="Starters", image="https://i.pinimg.com/236x/bf/82/05/bf82057cdd3c47275717dd04b17cc6b0.jpg"),
            Category(category_name="Main Course", image="https://i.pinimg.com/236x/eb/6e/ec/eb6eecacd7a45143b9af85eb37468961.jpg"),
            Category(category_name="Salads", image="https://i.pinimg.com/564x/f2/16/f0/f216f08940e8370d07f2295285a952df.jpg"),
            Category(category_name="Desserts", image="https://i.pinimg.com/564x/9d/25/93/9d2593780fe22eba7acf1ea6e9e57110.jpg"),
        ]
        db.session.add_all(categories)
        db.session.commit()

        print("Categories added successfully")
