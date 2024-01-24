from flask import Flask, abort, flash, redirect, render_template, request, url_for
from os import environ
from db.schema import db, User, Category, Product, Order, Order_item


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL') 
app.secret_key = 'D0018E' # så att flash fungerar

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
    return render_template("show_product.html", product=product)

'''Return the cart page'''
@app.route('/cart')
def Cart():
    return 'Cart Page'

'''Return the all categories page'''
@app.route('/categories')
def Categories():
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)

'''Return the specific category Page'''
@app.route('/categories/<int:id>')
def Specific_category(id):
    category = Category.query.filter_by(id=id).first()
    if Category is None:
        return "Category not found"
    return render_template("show_category.html", category=category)

'''Return the login page'''
@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate the inputs (you can add more validation if needed)
        if not email or not password:
            flash('Please enter all the fields', 'error')
        else:
            # Check if the user exists in the database
            user = User.query.filter_by(email=email).first()

            if user:
                # Validate Password
                if user.password == password:
                    flash('Successfully logged in', 'success')
                    return redirect(url_for('Home'))
    return render_template("login.html")

'''Return the register page'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate the inputs (you can add more validation if needed)
        if not name or not email or not password:
            flash('Please enter all the fields', 'error')
        elif User.query.filter_by(name=name).first():
            flash('Name already exists', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
        else:


            # Create a new user and add them to the database
            user = User(name=name, email=email, password=password, admin=False)
            db.session.add(user)
            db.session.commit()

            flash('Successfully registered', 'success')
            return redirect(url_for('Login'))  # Redirect to the login page

    else:
        return render_template("register.html")

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