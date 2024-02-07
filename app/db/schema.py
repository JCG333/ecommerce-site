'''
This file contains the schema of the database
'''
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

'''
Table that stores the user information
attributes:
    name: name of the user
    email: email of the user
    password: password of the user
    admin: boolean value that indicates if the user is an admin or not
'''
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    admin = db.Column(db.Boolean)

    def __init__(self, name, email, password, admin):
        self.admin = admin
        self.name = name
        self.email = email
        self.password = password

'''
Table that stores the category information
attributes:
    category_name: name of the category
    parent_category_id: parent category id of the category
'''
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(32), unique=True)

    parent_category_id = db.Column(db.Integer, ForeignKey('category.id'))

    def __init__(self, category_name, parent_category_id):
        self.category_name = category_name
        self.parent_category_id = parent_category_id
        
    def json(self):
        return {'id': self.id, 'name': self.name}

'''
Table that stores the product information

attributes:
    name: name of the product
    price: price of the product
    description: description of the product
    image: image of the product
    quantity: quantity of the product
    category_id: category id of the product
'''
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Float)
    description = db.Column(db.String(64))
    image = db.Column(db.String(64))
    quantity = db.Column(db.Integer)

    category_id = db.Column(db.Integer, ForeignKey('category.id'))

    def __init__(self, name, price, description, image, quantity, category_id):
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.quantity = quantity
        self.category_id = category_id
    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'description': self.description, 'image': self.image, 'quantity': self.quantity, 'category_id': self.category_id}

'''
Table that stores the review information
attributes:
    user_id: user id of the user
    product_id: product id of the product
    rating: rating of the product
    comment: comment of the product
    created_at: date of the review
'''
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    product_id = db.Column(db.Integer, ForeignKey('products.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship('User', backref='Review')
    product = relationship('Product', backref='Review')

    def __init__(self, user_id, product_id, rating, comment):
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment
    
    def json(self):
        return {'id': self.id, 'rating': self.rating, 'comment': self.comment, 'created_at': self.created_at, 'user_name': self.user.name}

'''
Table that stores the order information
attributes:
    order_date: date of the order
    shipping_address: shipping address of the order
    user_id: user id of the user
'''
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    shipping_address = db.Column(db.String(64))

    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    user = relationship('User', backref='Order')

    def __init__(self, user_id):
        self.user_id = user_id
    def json(self):
        return {'id': self.id, 'order_date': self.order_date, 'shipping_address': self.shipping_address, 'user_name': self.user.name}

'''
Table that stores the order item information
attributes:
    product_id: product id of the product
    order_id: order id of the order
    quantity: quantity of the product
'''
class Order_item(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('products.id'))
    order_id = db.Column(db.Integer, ForeignKey('orders.id'))
    quantity = db.Column(db.Integer)

    product = relationship('Product', backref='Order_item')
    order = relationship('Order', backref='Order_item')

    def __init__(self, product_id, quantity, order_id):
        self.product_id = product_id
        self.quantity = quantity
        self.order_id = order_id
    def json(self):
        return {'id': self.id, 'product_name': self.product.name,'product_id': self.product_id, 'quantity': self.quantity, 'order_id': self.order_id}

