from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify, make_response, session
from os import environ
from db.schema import db, User, Category, Product, Order, Order_item, Review


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL') 
app.secret_key = 'D0018E' # så att flash fungerar

def create_tables():
    with app.app_context():
        db.init_app(app)
        db.create_all()

        # Add default entries if they're not already in the database
        if not User.query.first() and not Product.query.first() and not Category.query.first() and not Review.query.first():
            try:
                category1 = Category(category_name ='T-Shirts', parent_category_id = None)
                db.session.add(category1)
                db.session.commit()

                product1 = Product(name ='T-Shirt', price =25.00, description ='This is a T-Shirt.', image ='images/t-shirts/shrek_t-shirts_1.png', quantity =10, category_id=category1.id)
                db.session.add(product1)
                product2 = Product(name ='Shrek running t-shirt', price =50.00, description ='This is a T-Shirt of Shrek running.', image ='images/t-shirts/shrek_t-shirts_2.png', quantity =30, category_id=category1.id)
                db.session.add(product2)
                product3 = Product(name ='Cool Shrek t-shirt', price =125.00, description ='This is a T-Shirt of Shrek being cool.', image ='images/t-shirts/shrek_t-shirts_3.png', quantity =5, category_id=category1.id)
                db.session.add(product3)
                db.session.commit()

                admin = User(name='admin', email='admin@shrek.com', password='abc123', admin=True)
                db.session.add(admin)
                db.session.commit()

                review = Review(product_id=product1.id, user_id=admin.id, rating=5, comment='This is a great product')
                db.session.add(review)
                db.session.commit()

                print('Default entries added successfully')
            
            except Exception as e:
                print('Error occured:', e)

create_tables()


'''
= Create a new order item and add to cart =
product_id: id of the product
quantity: quantity of the product
user_id: id of the user 
'''
@app.route('/create_orderItem', methods=['POST'])
def create_orderItem() -> str:
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

'''
= Return a specific product page =
id: id of the product
'''
@app.route('/products/<int:id>')
def Specific_Product(id) -> str:
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return "Product not found"
    return render_template("show_product.html", product=product)

'''Return the cart page'''
@app.route('/cart')
def Cart():
    return 'Cart Page'

'''
= Return the specific category Page =
category_name: name of the category
'''
@app.route('/categories/<category_name>', methods=['GET'])
def Specific_category(category_name) -> str:
    # get category from the database
    try:
        category = Category.query.filter_by(category_name=category_name).first()
        if category is None:
            return "Category not found"
        return render_template("show_category.html", category=category)
    except Exception as e:
        return make_response(jsonify({'message': 'error finding category', 'error': str(e)}), 404)

'''
= Return the login page =
email: email of the user
password: password of the user
'''

@app.route('/login', methods=['POST'])
def Login() -> str:
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
@app.route('/myaccount')
def MyAccount():
    return render_template("account.html")  

'''Return the checkout page'''
@app.route('/checkout')
def Checkout():
    return 'Checkout Page'

'''Return the admin page'''
@app.route('/admin')
def Admin():
    return 'Admin Page'

'''Logout the user'''
@app.route('/logout', methods=['GET'])
def Logout():
    try:
        session.clear()
        return make_response(jsonify({'message': 'Successfully logged out'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error logging out', 'error': str(e)}), 500)
    
'''
= Return reviews for a specific product =
product_id: id of the product
reviews: list of reviews for the product
'''
@app.route('/reviews/<int:id>', methods=['GET'])
def get_reviews(id) -> str:
    try:
        reviews = Review.query.filter_by(product_id=id).all()
        return make_response(jsonify({'reviews': [review.json() for review in reviews]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting reviews', 'error': str(e)}), 500)

'''
= Create reviews for a specific product =
product_id: id of the product
user_id: id of the user
rating: rating of the product
comment: comment of the product
'''
@app.route('/post_review/<int:id>', methods=['PUT'])
def post_reviews(id) -> str:
    try:
        request.get_json()
        user_id = session['user_id']
        rating = request.json.get('rating')
        comment = request.json.get('comment')
        review = Review(product_id=id, user_id=user_id, rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()
        return make_response(jsonify({'message': 'Successfully posted review'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error posting review', 'error': str(e)}), 500)


'''
= Return average rating =
id: id of the product
reviews: list of reviews for the product
average: average rating of the product
'''
@app.route('/average_rating/<int:id>', methods=['GET'])
def average_rating(id) -> str:
    try:
        reviews = Review.query.filter_by(product_id=id).all()
        if reviews:
            average = sum(review.rating for review in reviews) / len(reviews)
        else:
            average = 0
        return make_response(jsonify({'average': average}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting average rating', 'error': str(e)}), 500)
    
'''
= Return number of reviews =
id: id of the product
reviews: list of reviews for the product
'''
@app.route('/number_of_reviews/<int:id>', methods=['GET'])
def number_of_reviews(id) -> str:
    try:
        reviews = Review.query.filter_by(product_id=id).all()
        return make_response(jsonify({'number_of_reviews': len(reviews)}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting number of reviews', 'error': str(e)}), 500)
    
'''
= return the search results =
search_term: search term
products: list of products that match the search term
'''
@app.route('/search/<search_term>', methods=['GET'])
def search(search_term):
    try:
        products = Product.query.filter(Product.name.ilike('%' + search_term + '%')).all()
        if len(products) > 0:
            return render_template("search_results.html", products=products)
        return render_template("search_results.html", products=None)
    except Exception as e:
        return make_response(jsonify({'message': 'error searching', 'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)