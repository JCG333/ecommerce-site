from flask import Flask, abort
from db.schema import db, User, Category, Products, Cart, orders

app = Flask(__name__)

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