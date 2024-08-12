
from app import app
from models import Admin, Meal, Category, db
from flask_bcrypt import Bcrypt

# Initialize the Bcrypt instance
bcrypt = Bcrypt(app)

admin_list = [
    {'username': 'Levis Rabah', 'email': 'levisrabah@gmail.com', 'password': 'rabah9598'},
    {'username': 'Elvis Moses', 'email': 'elvis@gmail.com', 'password': 'elvo123'},
    {'username': 'Meshack Orina', 'email': 'mesh@gmail.com', 'password': 'orina456'},
    {'username': 'Allan Too', 'email': 'allan@gmail.com', 'password': 'allan2024'},
    {'username': 'Arnold Maina', 'email': 'arnold@gmail.com', 'password': 'arnold2024'}
]

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Add admin users to the database
        admins = []
        for admin in admin_list:
            hashed_password = bcrypt.generate_password_hash(admin['password']).decode('utf-8')
            new_admin = Admin(
                username=admin['username'],
                email=admin['email'],
                password_hash=hashed_password,
            )
            admins.append(new_admin)
        
        db.session.add_all(admins)
        db.session.commit()
        print("Admins added successfully")

        
        categories=[
            Category(category_name="APPETIZERS", description='Flavorful dishes served before the main course to stimulate the appetite. These can range from bite-sized finger foods to light salads, offering a variety of tastes and textures to enhance the dining experience.', image="https://i.pinimg.com/564x/c7/cd/0b/c7cd0b4802aa989e48706dfb6cfd77cc.jpg"),
            Category(category_name="STATERS", description='These are designed to stimulate the appetite, often light and flavorful, such as soups, salads, or finger foods like bruschetta or shrimp cocktail.', image="https://i.pinimg.com/564x/76/8b/d6/768bd63188b642699bd3bf8bce59222a.jpg"),
            Category(category_name="MAIN COURSE", description='The Main Course category features hearty and substantial dishes that serve as the centerpiece of a meal. Typically including proteins like meat, fish, or plant-based alternatives, these dishes are often accompanied by sides such as vegetables, grains, or sauces, making them the most filling and satisfying part of the dining experience', image="https://i.pinimg.com/564x/95/de/02/95de0207010fac62b549df3f526e5006.jpg"),
            Category(category_name="SALADS", description='The Salads category features fresh, vibrant dishes that combine crisp vegetables, leafy greens, and a variety of toppings like fruits, nuts, and cheeses. These meals are often dressed with light vinaigrettes or creamy dressings, offering a healthy and flavorful option for any time of the day. Perfect for a refreshing meal or a side dish, our salads cater to diverse tastes with both classic and creative combinations.', image="https://i.pinimg.com/564x/8f/19/62/8f1962a32091e211bc010eef7525a83a.jpg"),
            Category(category_name="DESSERTS", description='The Desserts category features a delectable selection of sweet treats, including cakes, pastries, ice creams, and more, perfect for satisfying your sweet tooth and ending your meal on a delightful note', image="https://i.pinimg.com/564x/9d/25/93/9d2593780fe22eba7acf1ea6e9e57110.jpg"),
        ]
        db.session.add_all(categories)
        db.session.commit()

        print("Categories added successfully")

        meals = [
            # Appetizers
            Meal(name="Bruschetta", description="Grilled bread with tomatoes and basil", price=5.99, admin_id=1, category_id=1, image='https://i.pinimg.com/236x/4c/22/08/4c22083319034ab9d64d244819be8683.jpg'),
            Meal(name="Stuffed Mushrooms", description="Mushrooms stuffed with cheese and herbs", price=6.99, admin_id=2, category_id=1, image='https://i.pinimg.com/236x/40/0b/a8/400ba84241c949b869fe998920617cb5.jpg'),
            Meal(name="Garlic Bread", description="Bread with garlic and butter", price=3.99, admin_id=3, category_id=1, image='https://i.pinimg.com/236x/3b/78/86/3b7886c8f78bf4e9a03ea7ce619f693c.jpg'),
            Meal(name="Chicken Wings", description="Spicy chicken wings", price=8.99, admin_id=4, category_id=1, image='https://i.pinimg.com/236x/3c/e0/5d/3ce05d755f2116bae850cd377e26dbef.jpg'),
            Meal(name="Spring Rolls", description="Crispy rolls with vegetables", price=5.99, admin_id=5, category_id=1, image='https://i.pinimg.com/236x/a5/7a/da/a57ada9962153de831f02e5d2f643797.jpg'),
            Meal(name="Mozzarella Sticks", description="Fried mozzarella cheese sticks", price=7.99, admin_id=1, category_id=1, image='https://i.pinimg.com/236x/01/9c/48/019c48138e87de3285c4581c50b3c32f.jpg'),
            Meal(name="Nachos", description="Tortilla chips with cheese and salsa", price=6.99, admin_id=2, category_id=1, image='https://i.pinimg.com/236x/33/32/bd/3332bdbf432a6daffc1304b485acb64e.jpg'),
            Meal(name="Onion Rings", description="Crispy fried onion rings", price=4.99, admin_id=3, category_id=1, image='https://i.pinimg.com/236x/00/92/6b/00926bbec43edce93643f4eafa21312b.jpg'),
            Meal(name="Potato Skins", description="Potato skins with cheese and bacon", price=7.99, admin_id=4, category_id=1, image='https://i.pinimg.com/236x/44/ff/3f/44ff3f471d3c7a006a8b626359d72cfb.jpg'),
            Meal(name="Quesadilla", description="Grilled tortilla with cheese and chicken", price=8.99, admin_id=5, category_id=1, image='https://i.pinimg.com/236x/5a/98/35/5a9835137deff27d2022fdb393fad7f0.jpg'),
            Meal(name="Mini Tacos", description="Small tacos with beef and cheese", price=6.99, admin_id=1, category_id=1, image='https://i.pinimg.com/236x/1a/9f/de/1a9fde24f25d1f7df44e85c900ef37d8.jpg'),
            Meal(name="Crab Cakes", description="Fried crab cakes with sauce", price=9.99, admin_id=2, category_id=1, image='https://i.pinimg.com/236x/a0/62/40/a06240ced032c37e33fe45afb388e724.jpg'),
            Meal(name="Shrimp Cocktail", description="Chilled shrimp with cocktail sauce", price=10.99, admin_id=3, category_id=1, image='https:// i.pinimg.com/236x/ba/c6/9f/bac69f2e406c17e6f2cf2d30c9f2bbb8.jpg'),
            Meal(name="Cheese Platter", description="Assorted cheeses with crackers", price=12.99, admin_id=4, category_id=1, image='https://i.pinimg.com/236x/47/09/8c/47098ca62627836ea1c98664696ac228.jpg'),
            Meal(name="Deviled Eggs", description="Eggs with a creamy filling", price=5.99, admin_id=5, category_id=1, image='https://i.pinimg.com/236x/e5/4c/37/e54c37772f562385aee66a0d1cf7cab0.jpg'),
            Meal(name="Hummus Plate", description="Hummus with pita bread and vegetables", price=6.99, admin_id=1, category_id=1, image='https://i.pinimg.com/236x/9f/9e/7d/9f9e7d5b313c1bc652bbd4e392a1b415.jpg'),
            Meal(name="Meatballs", description="Italian-style meatballs with sauce", price=8.99, admin_id=2, category_id=1, image='https://i.pinimg.com/236x/ae/be/29/aebe2945a187846a87b03f5f29ca2d6d.jpg'),
            Meal(name="Caprese Skewers", description="Tomato, basil, and mozzarella on skewers", price=7.99, admin_id=3, category_id=1, image='https://i.pinimg.com/236x/a4/58/7c/a4587c4bc84280b3ccbc917495352690.jpg'),
            Meal(name="Spinach Dip", description="Creamy spinach dip with bread", price=6.99, admin_id=4, category_id=1, image='https://i.pinimg.com/236x/19/28/ed/1928ede2a28edb9884dd79ea3d217d91.jpg'),
            Meal(name="Fruit Platter", description="Assorted fresh fruits", price=9.99, admin_id=5, category_id=1, image='https://i.pinimg.com/236x/ae/ec/d0/aeecd05db9d49e23d80bf66371608b37.jpg'),
            
            # Starters
            Meal(name="Tomato Soup", description="Creamy tomato soup with croutons", price=4.99, admin_id=1, category_id=2, image='https://i.pinimg.com/236x/b4/04/c5/b404c577cce4a40ae4f3b733be5d87be.jpg'),
            Meal(name="French Onion Soup", description="Onion soup with melted cheese", price=5.99, admin_id=2, category_id=2, image='https://i.pinimg.com/236x/61/c2/32/61c2323f61cf61217ebecb6d092cd158.jpg'),
            Meal(name="Caesar Salad", description="Romaine lettuce with Caesar dressing", price=6.99, admin_id=3, category_id=2, image='https://i.pinimg.com/236x/03/2c/c0/032cc09f6476e397c588b91fca0c8a10.jpg'),
            Meal(name="House Salad", description="Mixed greens with dressing", price=5.99, admin_id=4, category_id=2, image='https://i.pinimg.com/474x/34/8f/70/348f70d313535cc415eb170849230f13.jpg'),
            Meal(name="Minestrone Soup", description="Vegetable soup with pasta", price=4.99, admin_id=5, category_id=2, image='https://i.pinimg.com/236x/6b/e3/60/6be3604e1c69c20c82c9ef8d70b19b14.jpg'),
            Meal(name="Clam Chowder", description="Creamy clam chowder", price=6.99, admin_id=1, category_id=2, image='https://i.pinimg.com/236x/1d/90/12/1d9012b7b7a2c65fd5945d4ecbf053e7.jpg'),
            Meal(name="Greek Salad", description="Salad with feta cheese and olives", price=6.99, admin_id=2, category_id=2, image='https://i.pinimg.com/236x/8e/40/37/8e4037fa655532a5b2d4cee38415f1e8.jpg'),
            Meal(name="Lobster Bisque", description="Rich lobster bisque", price=7.99, admin_id=3, category_id=2, image='https://i.pinimg.com/236x/71/ff/23/71ff23916238fdedc560d305cdb3ce7b.jpg'),
            Meal(name="Caprese Salad", description="Tomatoes, mozzarella, and basil", price=7.99, admin_id=4, category_id=2, image='https://i.pinimg.com/236x/70/f8/93/70f893bd8b4b63449771fb5562bfae55.jpg'),
            Meal(name="Chicken Noodle Soup", description="Classic chicken noodle soup", price=4.99, admin_id=5, category_id=2, image='https://i.pinimg.com/236x/0a/5f/64/0a5f64de2183d53305468e0bd1067ca4.jpg'),
            Meal(name="Beef Carpaccio", description="Thinly sliced raw beef", price=9.99, admin_id=1, category_id=2, image='https://i.pinimg.com/236x/3d/96/e2/3d96e2f3e97953ab6729dfa47f48f5bc.jpg'),
            Meal(name="Shrimp Scampi", description="Shrimp in garlic butter sauce", price=8.99, admin_id=2, category_id=2, image='https://i.pinimg.com/236x/8b/da/dc/8bdadcff724d828c7311bc85e21d8ffe.jpg'),
            Meal(name="Egg Drop Soup", description="Chinese egg drop soup", price=4.99, admin_id=3, category_id=2, image='https://i.pinimg.com/236x/41/59/69/4159696f1893ad916415dcce33b8afaa.jpg'),
            Meal(name="Tuna Tartare", description="Raw tuna with avocado and sauce", price=10.99, admin_id=4, category_id=2, image='https://i.pinimg.com/474x/ca/69/30/ca693014d2974753aa94174f0696c1cb.jpg'),
            Meal(name="Wedge Salad", description="Iceberg lettuce with blue cheese", price=6.99, admin_id=5, category_id=2, image='https://i.pinimg.com/236x/ec/78/44/ec7844991cb5c0a7ac278bc00857f360.jpg'),
            Meal(name="Vegetable Soup", description="Healthy vegetable soup", price=4.99, admin_id=1, category_id=2, image='https://i.pinimg.com/236x/f0/95/79/f0957903755b91f0885010c36f47e91d.jpg'),
            Meal(name="Crab Soup", description="Soup with crab meat", price=6.99, admin_id=2, category_id=2, image='https://i.pinimg.com/236x/82/ed/7f/82ed7f568ce297325d769e9931e49552.jpg'),
            Meal(name="Beet Salad", description="Salad with beets and goat cheese", price=7.99, admin_id=3, category_id=2, image='https://i.pinimg.com/236x/3e/96/cb/3e96cba4e3239ceacd5a579b8a564625.jpg'),
            Meal(name="Miso Soup", description="Japanese miso soup", price=3.99, admin_id=4, category_id=2, image='https://i.pinimg.com/236x/ae/7c/0a/ae7c0a958ad45d99470de24537dbb9cd.jpg'),
            Meal(name="Pumpkin Soup", description="Creamy pumpkin soup", price=4.99, admin_id=5, category_id=2, image='https://i.pinimg.com/236x/69/c3/60/69c360b6d8b0805bfbeb548a90906ec6.jpg'),

            # Main Meals
            Meal(name="Fried Rice", description="Fried rice with chicken and vegetables", price=10.99, admin_id=1, category_id=3, image='https://i.pinimg.com/236x/d5/5d/df/d55ddf495e2db4e627654827dd98882e.jpg'),
            Meal(name="Grilled Chicken", description="Grilled chicken with herbs", price=12.99, admin_id=2, category_id=3, image='https://i.pinimg.com/236x/b1/e6/ae/b1e6ae89ae2c3b209ca867ff8de3c3dd.jpg'),
            Meal(name="Beef Steak", description="Juicy beef steak with sauce", price=15.99, admin_id=3, category_id=3, image='https://i.pinimg.com/236x/6d/99/0a/6d990a457ee61c0cb1b32d21ed147f40.jpg'),
            Meal(name="Spaghetti Bolognese", description="Pasta with meat sauce", price=11.99, admin_id=4, category_id=3, image='https://i.pinimg.com/236x/b8/19/7d/b8197df436e0bd3a7493bf2fe5429c81.jpg'),
            Meal(name="Chicken Caesar Salad", description="Salad with grilled chicken", price=9.99, admin_id=5, category_id=3, image='https://i.pinimg.com/236x/64/e6/d5/64e6d5b54878240a579a712ada49c409.jpg'),
            Meal(name="BBQ Ribs", description="Barbecue ribs with sauce", price=14.99, admin_id=1, category_id=3, image='https://i.pinimg.com/236x/fd/18/19/fd1819a0d190eb2b110eb148854325f6.jpg'),
            Meal(name="Fish Tacos", description="Tacos with fish and vegetables", price=11.99, admin_id=2, category_id=3, image='https://i.pinimg.com/236x/07/74/b1/0774b1109877cf9bb54609230cc817d0.jpg'),
            Meal(name="Vegetable Stir Fry", description="Stir-fried vegetables with sauce", price=10.99, admin_id=3, category_id=3, image='https://i.pinimg.com/236x/f7/8b/b8/f78bb8c02fa648cf5966ecff1ec89e25.jpg'),
            Meal(name="Pasta Carbonara", description="Pasta with creamy sauce", price=12.99, admin_id=4, category_id=3, image='https://i.pinimg.com/236x/93/44/17/934417511333c93de13318c34cf208e8.jpg'),
            Meal(name="Cheeseburger", description="Burger with cheese and toppings", price=9.99, admin_id=5, category_id=3, image='https://i.pinimg.com/236x/25/1e/6e/251e6e605f5b1a93f179a560592b050f.jpg'),
            Meal(name="Shrimp Alfredo", description="Pasta with shrimp and Alfredo sauce", price=13.99, admin_id=1, category_id=3, image='https://i.pinimg.com/236x/43/20/e0/4320e050f80fca91fafff0a336928e34.jpg'),
            Meal(name="Chicken Parmesan", description="Chicken with marinara sauce and cheese", price=12.99, admin_id=2, category_id=3, image='https://i.pinimg.com/236x/0a/d2/d9/0ad2d966378d03350a0bcfd220a8f11f.jpg'),
            Meal(name="Lasagna", description="Layered pasta with meat and cheese", price=14.99, admin_id=3, category_id=3, image='https://i.pinimg.com/236x/6e/04/05/6e0405bc7c4b4430077603049773440f.jpg'),
            Meal(name="Pork Chops", description="Grilled pork chops with sauce", price=13.99, admin_id=4, category_id=3, image='https://i.pinimg.com/236x/ab/00/d8/ab00d8cdc9392bdf4c789bfc2effcbd0.jpg'),
            Meal(name="Turkey Sandwich", description="Sandwich with turkey and cheese", price=8.99, admin_id=5, category_id=3, image='https://i.pinimg.com/236x/1b/34/2c/1b342cd5f92f1b8aa8c14d522d78f95d.jpg'),
            Meal(name="Salmon Fillet", description="Grilled salmon with lemon", price=15.99, admin_id=1, category_id=3, image='https://i.pinimg.com/236x/44/6a/f0/446af0cee1d8a4e77b635552db5b81f2.jpg'),
            Meal(name="Lamb Chops", description="Grilled lamb chops with rosemary", price=16.99, admin_id=2, category_id=3, image='https://i.pinimg.com/236x/ed/1c/91/ed1c91ff61c3efc1bd2ec57d8ac02747.jpg'),
            Meal(name="Beef Stroganoff", description="Beef with creamy sauce and noodles", price=13.99, admin_id=3, category_id=3, image='https://i.pinimg.com/236x/84/27/2a/84272a11687da222bd9072270dfd3156.jpg'),
            Meal(name="Chicken Tikka Masala", description="Chicken in spiced curry sauce", price=14.99, admin_id=4, category_id=3, image='https://i.pinimg.com/236x/c6/65/c7/c665c758a0b5d5a6a93db951d11124d1.jpg'),
            Meal(name="Veggie Burger", description="Burger with vegetables and toppings", price=10.99, admin_id=5, category_id=3, image='https://i.pinimg.com/236x/46/c4/08/46c408fd69c74b2e44dced39bed26411.jpg'),
            Meal(name="Vegetarian Pizza", description="Pizza with assorted vegetables", price=12.99, admin_id=1, category_id=3, image='https://i.pinimg.com/236x/a6/8b/61/a68b61bff6c375103e1fa96385d34ecb.jpg'),
            Meal(name="Chicken Fajitas", description="Chicken fajitas with peppers and onions", price=13.99, admin_id=2, category_id=3, image='https://i.pinimg.com/236x/7e/50/0b/7e500b1f6a385d3d6463f11cb779595e.jpg'),
            Meal(name="Beef Burrito", description="Burrito with beef, beans, and rice", price=11.99, admin_id=3, category_id=3, image='https://i.pinimg.com/236x/c8/e2/ac/c8e2ac94b991a84a01b76d56957b8ba9.jpg'),
            Meal(name="Lamb Gyro", description="Gyro with lamb and tzatziki sauce", price=14.99, admin_id=4, category_id=3, image='https://i.pinimg.com/236x/7e/46/11/7e4611586b86eb5563db731d7824e3e5.jpg'),
            Meal(name="Seafood Paella", description="Paella with assorted seafood", price=18.99, admin_id=5, category_id=3, image='https://i.pinimg.com/236x/f5/12/01/f5120114b830a837c6802e7b29244ad4.jpg'),
            Meal(name="Vegetable Curry", description="Curry with mixed vegetables", price=10.99, admin_id=1, category_id=3, image='https://i.pinimg.com/236x/b9/63/8c/b9638c5a2ba1d325a24d21c765a04b71.jpg'),
            Meal(name="Stuffed Peppers", description="Peppers stuffed with rice and beef", price=12.99, admin_id=2, category_id=3, image='https://i.pinimg.com/236x/20/dd/98/20dd98d752c6769f4b22ff3e0eeec867.jpg'),
            Meal(name="Pad Thai", description="Thai noodles with shrimp and peanuts", price=13.99, admin_id=3, category_id=3, image='https://i.pinimg.com/236x/6a/07/1a/6a071ab6a628d73eb3fb4d3db83be920.jpg'),
            Meal(name="Ratatouille", description="French vegetable stew", price=11.99, admin_id=4, category_id=3, image='https://i.pinimg.com/236x/06/65/23/066523e3b07f1a6c4a107bd8516057c6.jpg'),
            Meal(name="Steak Frites", description="Steak with fries and sauce", price=16.99, admin_id=5, category_id=3, image='https://i.pinimg.com/236x/16/03/62/16036201a60cb0e493e730f0f0d7fc04.jpg'),

            # Salads
            Meal(name="Caesar Salad", description="Romaine lettuce with Caesar dressing", price=7.99, admin_id=1, category_id=4, image='https://i.pinimg.com/236x/07/b3/fa/07b3fa5f80454a92f323140a4504ad23.jpg'),
            Meal(name="Greek Salad", description="Salad with feta cheese and olives", price=8.99, admin_id=2, category_id=4, image='https://i.pinimg.com/236x/16/f9/85/16f9858fe1ade6fe992a0ab06dd345f7.jpg'),
            Meal(name="Caprese Salad", description="Tomatoes, mozzarella, and basil", price=9.99, admin_id=3, category_id=4, image='https://i.pinimg.com/236x/08/f9/e4/08f9e4cf15c6d2214f8bd6860b160f9b.jpg'),
            Meal(name="Cobb Salad", description="Salad with chicken, bacon, and eggs", price=10.99, admin_id=4, category_id=4, image='https://i.pinimg.com/236x/b3/cf/19/b3cf19909aa8f203ccad98dd401e8b36.jpg'),
            Meal(name="Garden Salad", description="Mixed greens with vegetables", price=6.99, admin_id=5, category_id=4, image='https://i.pinimg.com/236x/44/bb/ef/44bbef48a6c656bb9af152e7baef67db.jpg'),
            Meal(name="Spinach Salad", description="Spinach with strawberries and nuts", price=8.99, admin_id=1, category_id=4, image='https://i.pinimg.com/236x/5f/10/58/5f1058a3c467f0cd525b565bba20eba0.jpg'),
            Meal(name="Kale Salad", description="Kale with cranberries and almonds", price=8.99, admin_id=2, category_id=4, image='https://i.pinimg.com/236x/18/c6/57/18c6577f41595c85e34cd3efe3678cc3.jpg'),
            Meal(name="Quinoa Salad", description="Quinoa with vegetables and feta", price=9.99, admin_id=3, category_id=4, image='https://cdn.loveandlemons.com/wp-content/uploads/2020/08/quinoa-salad.jpg'),
            Meal(name="Taco Salad", description="Salad with taco ingredients", price=10.99, admin_id=4, category_id=4, image='https://i.pinimg.com/236x/b0/47/62/b047622da5d3a608f85b2d05c59fa886.jpg'),
            Meal(name="Pasta Salad", description="Cold pasta with vegetables", price=7.99, admin_id=5, category_id=4, image='https://i.pinimg.com/236x/84/b4/86/84b486780d565df0f8478bd866fedae5.jpg'),
            Meal(name="Chicken Salad", description="Salad with chicken and mayonnaise", price=9.99, admin_id=1, category_id=4, image='https://i.pinimg.com/236x/ea/11/7d/ea117d3cc11a22f926a7d36f4232057c.jpg'),
            Meal(name="Broccoli Salad", description="Salad with broccoli and bacon", price=8.99, admin_id=2, category_id=4, image='https://i.pinimg.com/236x/f2/d0/17/f2d017d171056969f16eeb7585d77a53.jpg'),
            Meal(name="Fruit Salad", description="Mixed fresh fruits", price=7.99, admin_id=3, category_id=4, image='https://i.pinimg.com/236x/a7/1f/ae/a71fae78038cdd5c95c279186a580717.jpg'),
            Meal(name="Beet Salad", description="Salad with beets and goat cheese", price=8.99, admin_id=4, category_id=4, image='https://i.pinimg.com/236x/aa/b4/f6/aab4f6b08e179dcdc2c48b35550d709f.jpg'),
            Meal(name="Asian Salad", description="Salad with Asian-style dressing", price=9.99, admin_id=5, category_id=4, image='https://i.pinimg.com/474x/29/41/da/2941da810b81c38e40829b7591758213.jpg'),
            Meal(name="Avocado Salad", description="Salad with avocado and greens", price=10.99, admin_id=1, category_id=4, image='https://i.pinimg.com/236x/63/cb/22/63cb22a28b06f30e8bc847665c14671f.jpg'),
            Meal(name="Nicoise Salad", description="Salad with tuna, eggs, and olives", price=11.99, admin_id=2, category_id=4, image='https://i.pinimg.com/236x/0d/f2/d5/0df2d5cb225019fcceb8d134e4417e84.jpg'),
            Meal(name="Lentil Salad", description="Salad with lentils and vegetables", price=8.99, admin_id=3, category_id=4, image='https://i.pinimg.com/236x/16/3c/e0/163ce0b3bc42278906dae11bd52a8158.jpg'),
            Meal(name="Southwest Salad", description="Salad with corn, beans, and avocado", price=9.99, admin_id=4, category_id=4, image='https://i.pinimg.com/236x/2d/ab/e3/2dabe37322b837adc6e7ad93aaec2aef.jpg'),
            Meal(name="Cauliflower Salad", description="Salad with roasted cauliflower", price=8.99, admin_id=5, category_id=4, image='https://i.pinimg.com/236x/3d/0b/35/3d0b350f6709dd82b9040de436e0cb7c.jpg'),

            # Desserts
            Meal(name="Chocolate Cake", description="Rich chocolate cake with frosting", price=6.99, admin_id=1, category_id=5, image='https://i.pinimg.com/236x/fd/49/15/fd49150a45f56427ddc5da1da08861f4.jpg'),
            Meal(name="Cheesecake", description="Creamy cheesecake with a graham crust", price=7.99, admin_id=2, category_id=5, image='https://i.pinimg.com/236x/53/ff/e2/53ffe2ce6d416ba5dd9492580c4e8251.jpg'),
            Meal(name="Tiramisu", description="Classic Italian dessert with coffee", price=8.99, admin_id=3, category_id=5, image='https://i.pinimg.com/236x/f7/d7/71/f7d77137948b2bc40ec6d8a197580981.jpg'),
            Meal(name="Apple Pie", description="Apple pie with a flaky crust", price=5.99, admin_id=4, category_id=5, image='https://i.pinimg.com/236x/e2/e8/d5/e2e8d570bc477be1a4413f232d276375.jpg'),
            Meal(name="Ice Cream Sundae", description="Ice cream with toppings", price=4.99, admin_id=5, category_id=5, image='https://i.pinimg.com/236x/9f/ca/82/9fca828a192cc21d28f3f7715308b294.jpg'),
            Meal(name="Brownie", description="Chocolate brownie with nuts", price=3.99, admin_id=1, category_id=5, image='https://i.pinimg.com/236x/ae/05/e2/ae05e2aca2f2f3a7869027ab8d0fa49b.jpg'),
            Meal(name="Fruit Tart", description="Tart with fresh fruits", price=6.99, admin_id=2, category_id=5, image='https://i.pinimg.com/236x/af/d0/5c/afd05cf12e918d8ea0b3c47f5b8ec6fd.jpg'),
            Meal(name="Panna Cotta", description="Italian dessert with cream and berries", price=7.99, admin_id=3, category_id=5, image='https://i.pinimg.com/236x/c9/da/c0/c9dac0799a0afa7e15d26040339f225c.jpg'),
            Meal(name="Creme Brulee", description="Custard with a caramelized top", price=8.99, admin_id=4, category_id=5, image='https://i.pinimg.com/236x/b8/16/af/b816af22c30988d63b90e312e4717157.jpg'),
            Meal(name="Lemon Meringue Pie", description="Pie with lemon filling and meringue", price=5.99, admin_id=5, category_id=5, image='https://i.pinimg.com/236x/fe/a6/4b/fea64be986b7a3fd5c92abaa926f914c.jpg'),
            Meal(name="Carrot Cake", description="Spiced cake with cream cheese frosting", price=6.99, admin_id=1, category_id=5, image='https://i.pinimg.com/236x/4c/63/02/4c6302f4c0eb7b15ff0b55101644d6a0.jpg'),
            Meal(name="Banana Split", description="Ice cream with bananas and toppings", price=4.99, admin_id=2, category_id=5, image='https://i.pinimg.com/236x/5f/e6/53/5fe6531a7d752cc1ac25e95e6482937e.jpg'),
            Meal(name="Mousse", description="Light and fluffy chocolate mousse", price=7.99, admin_id=3, category_id=5, image='https://i.pinimg.com/236x/11/34/d0/1134d0055cb7d812fe082721230366a6.jpg'),
            Meal(name="Eclair", description="Pastry with cream filling", price=5.99, admin_id=4, category_id=5, image='https://i.pinimg.com/236x/8c/48/88/8c4888473d32c7f7680d573f15dde947.jpg'),
            Meal(name="Macarons", description="Colorful French macarons", price=8.99, admin_id=5, category_id=5, image='https://i.pinimg.com/236x/bf/d3/56/bfd3566b9d6a259ed9f5eae153cbb6b0.jpg'),
            Meal(name="Profiteroles", description="Pastry with ice cream filling", price=7.99, admin_id=1, category_id=5, image='https://i.pinimg.com/236x/9f/f7/e2/9ff7e2d2b458e338d36300ca955753c4.jpg'),
            Meal(name="Bread Pudding", description="Pudding with bread and raisins", price=6.99, admin_id=2, category_id=5, image='https://i.pinimg.com/236x/f0/92/4b/f0924be5584436f67f6d7590de6f3785.jpg'),
            Meal(name="Key Lime Pie", description="Pie with a lime filling", price=5.99, admin_id=3, category_id=5, image='https://i.pinimg.com/236x/64/00/38/640038b8aedb05a519af674e2ba3bf16.jpg'),
            Meal(name="Pavlova", description="Meringue dessert with fruits", price=8.99, admin_id=4, category_id=5, image='https://i.pinimg.com/236x/b7/97/f5/b797f55c677e052d2ea73ece92fd9795.jpg'),
            Meal(name="Sorbet", description="Frozen dessert with fruit flavors", price=4.99, admin_id=5, category_id=5, image='https://i.pinimg.com/236x/2b/d1/6c/2bd16cc5670e03b750e079ae7f5d6b39.jpg')
        ]

        db.session.add_all(meals)
        db.session.commit()

        print("Meals added successfully")
