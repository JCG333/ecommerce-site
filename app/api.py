from flask import Flask, abort
from os import environ
from db.schema import db, User, Category, Product, Order, Order_item

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL') 

def create_tables():
    with app.app_context():
        db.init_app(app)
        db.create_all()

create_tables()

'''Return the home page'''
@app.route('/')
def Home():
    return 'Home Page'

'''Return the all products page'''
@app.route('/products')
def Products():
    return 'All Products Page'

'''Return a specific product page'''
@app.route('/products/<int:id>')
def Product(id):
    product = Products.query.get(id)
    if product is None:
        abort(404)  # Not found
    return 'Specific Product Page'

'''Return the cart page'''
@app.route('/cart')
def Cart():
    return 'Cart Page'

'''Return the all categories page'''
@app.route('/categories')
def Categories():
    return 'All Categories page'

'''Return the specific category Page'''
@app.route('/categories/<int:id>')
def Category(id):
    return 'Specific Category Page'

'''Return the login page'''
@app.route('/login')
def Login():
    return 'Login Page'

'''Return the register page'''
@app.route('/register')
def Register():
    return 'Register Page'

'''Return your account page'''
@app.route('/myaccount/<int:id>')
def MyAccount(id):
    return 'My Account Page'   

'''Return the checkout page'''
@app.route('/checkout')
def Checkout():
    return 'Checkout Page'

'''Return the admin page'''
@app.route('/admin')
def Admin():
    return 'Admin Page'


if __name__ == '__main__':
    app.run(debug=True)