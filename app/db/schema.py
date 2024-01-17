from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    admin = db.Column(db.Boolean)

    def __init__(self, username, email, password, admin):
        self.admin = admin
        self.username = username
        self.email = email
        self.password = password

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Float)
    description = db.Column(db.String(64))
    image = db.Column(db.String(64))
    category = db.Column(db.String(32))

    def __init__(self, name, price, description, image, category):
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.category = category

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)

    def __init__(self, user_id, product_id, quantity, total_price):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price
