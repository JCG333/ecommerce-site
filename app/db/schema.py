from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

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

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(32))

    def __init__(self, category_name):
        self.category_name = category_name

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Float)
    description = db.Column(db.String(64))
    image = db.Column(db.String(64))
    category = db.Column(db.Integer, ForeignKey('category.id'))

    def __init__(self, name, price, description, image, category):
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.category = category

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    product_id = db.Column(db.Integer, ForeignKey('products.id'))

    user = relationship('User', backref='carts')
    product = relationship('Products', backref='carts')

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    product_id = db.Column(db.Integer, ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)

    user = relationship('User', backref='orders')
    product = relationship('Products', backref='orders')

    def __init__(self, user_id, product_id, quantity, total_price):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

