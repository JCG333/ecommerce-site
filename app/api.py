from flask import Flask, abort, request
from os import environ
from db.schema import db, User, Category, Product, Order, Order_item

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL') 

def create_tables():
    with app.app_context():
        db.init_app(app)
        db.create_all()

        try:
            category1 = Category(category_name ='T-Shirts', parent_category_id = None)
            db.session.add(category1)
            db.session.commit()

            product1 = Product(name ='T-Shirt', price =10.00, description ='This is a T-Shirt', image ='tshirt.jpg', quantity =10, category_id=category1.id)
            db.session.add(product1)
            db.session.commit()

            print('Default entries added successfully')
        
        except Exception as e:
            print('Didnt work', e)

create_tables()

'''Return the home page'''




@app.route('/')
def Home():
    return 'Home Page test'

'''Return the all products page'''
@app.route('/products')
def Products():
    return 'All Products Page'

'''Return a specific product page'''
@app.route('/products/<int:id>')
def Specific_Product(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return "Product not found"
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
@app.route('/register', methods=['GET', 'POST'])
def Register():
    if not all(key in request.form for key in ('username', 'email', 'password')):
        return "Not all parameters provided" #abort(400)
    user = User(
        username=request.form["username"],
        email=request.form["email"],
        password=request.form["password"],
        admin=False
    )
    db.session.add(user)
    db.session.commit()
    return 'User registered'
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
    app.run(host='0.0.0.0', port=5000, debug=True)