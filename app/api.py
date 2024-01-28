from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify, make_response, session
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

            product1 = Product(name ='T-Shirt', price =10.00, description ='This is a T-Shirt', image ='images/t-shirts/shrek_t-shirts_1.png', quantity =10, category_id=category1.id)
            db.session.add(product1)
            db.session.commit()

            admin = User(name='admin', email='admin@shrek.com', password='abc123', admin=True)
            db.session.add(admin)
            db.session.commit()

            print('Default entries added successfully')
        
        except Exception as e:
            print('Didnt work', e)

create_tables()


'''====== Create a new order item (if no order exists, create one, and add new item to it) ====='''

@app.route('/create_orderItem', methods=['POST'])
def create_orderItem():
    #get the product id and quantity from the request
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    #check if user is logged in, in current session
    if 'logged_in' not in session:
        return make_response(jsonify({'message': 'Please log in to add to cart'}), 401)

    #check if the order exists for logged in user
    user_id = session['user_id']
    order = Order.query.filter_by(user_id=user_id).first()
    try:
        if order is None:
            try:
                # If there is no existing order tied to logged in user
                new_order = Order(user_id=user_id)
                db.session.add(new_order)
                db.session.commit()
                order_item = Order_item(product_id=product_id, quantity=quantity, order_id=new_order.id)
                db.session.add(order_item)
                db.session.commit()
                return make_response(jsonify({'message': 'Successfully created order and added item'}), 200)
            except Exception as e:
                return make_response(jsonify({'message': 'error creating order and adding item', 'error': str(e)}), 500)
        else:
            try:
                # If there is an existing order tied to logged in user
                order_item = Order_item(product_id=product_id, quantity=quantity, order_id=order.id)
                db.session.add(order_item)
                db.session.commit()
                return make_response(jsonify({'message': 'Successfully added item to order'}), 200)
            except Exception as e:
                return make_response(jsonify({'message': 'error adding item to order', 'error': str(e)}), 500)
    except Exception as e:
        return make_response(jsonify({'message': 'error finding order', 'error': str(e)}), 404)

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


''' ========= Return the login page ======='''

@app.route('/login', methods=['POST'])
def Login():
    # Get the email and password from the request
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate the inputs
    if email is not None and password is not None:
        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # Validate Password
            if user.password == password:
                # Add user to the session
                session['logged_in'] = True
                session['user_id'] = user.id
                session['username'] = user.name
                return make_response(jsonify({'message': 'Successfully logged in', 'username': user.name}), 200)
            else:
                return make_response(jsonify({'message': 'Wrong password'}), 401)
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)
    else:
        return make_response(jsonify({'message': 'Please enter all the fields'}), 400)

'''Return the session user name'''
@app.route('/get_username', methods=['GET'])
def get_username():
    if 'username' in session:
        return jsonify({'username': session['username']})
    else:
        return jsonify({'username': None})

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
    app.run(host='0.0.0.0', port=4000, debug=True)