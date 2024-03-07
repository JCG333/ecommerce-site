import os
from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify, make_response, session
from os import environ
from db.schema import Review, db, User, Category, Product, Order, Order_item, Completed_orders, Completed_order_item

from random import randint


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL') 
app.secret_key = 'D0018E' # så att flash fungerar

descriptions_clothes = ['This is a great product made of 100% cotton', 'This is a fantastic product made of 100% wool',
                        'This is a quality product made out of the finest merinowool',
                        'This is a superb product made out of a blend consisting of 50% wool and 50% polyester ',
                        'This is an excellent product made out of plolyester and cotton', 'This is a quality product made out of the finest materials',]

descriptions_things = ['This is a great product', 'This is a fantastic product', 'This is a superb product made out of quality goods',
                       'This is an excellent product made out of the finest materials', 'This is a quality product made out of the finest materials',
                       'This is a superb product made out of the finest materials', 'This is a great product made out of the finest materials']

def create_tables():
    with app.app_context():
        db.init_app(app)
        db.create_all()
        images_folder = os.path.join(os.path.dirname(__file__), 'static/images')
        try:
            print('Adding default entries')
            # Loops through all the folders in the images folder and creates categories in the database
            for category_name in os.listdir(images_folder):
                category_path = os.path.join(images_folder, category_name)
                if os.path.isdir(category_path):
                    category = Category.query.filter_by(category_name=category_name).first()
                    if category is None:
                        print('adding a category')
                        category = Category(category_name=category_name, parent_category_id=None)
                        db.session.add(category)
                        db.session.commit()
                    # Loops through all the files in the category folder and creates products in the database
                    for product_name in os.listdir(category_path):
                        product_path = os.path.join(category_path, product_name)
                        if os.path.isfile(product_path):
                            print('product!')
                            product_name_no_ext = os.path.splitext(product_name)[0]  # Remove the file extension from the product name
                            product = Product.query.filter_by(name=product_name_no_ext).first()
                        # Check if the product already exists in the database and if the category is clothes    
                        if product is None and category_name in ['pants', 't-shirts', 'socks']:
                            print('product!!')
                            try:
                                image_path = os.path.join('images', category_name, product_name)
                                print('Adding products')
                                product = Product(name=product_name_no_ext, price=randint(99, 149), description=descriptions_clothes[randint(0,5)], image=image_path, quantity=randint(2,5), category_id=category.id)
                                db.session.add(product)
                                db.session.commit()
                            except Exception as e:
                                print(f"Error while adding product {product_name_no_ext}: {e}")
                                db.session.rollback() 

                        # Check if the product already exists in the database and if the category is things
                        elif product is None and category_name in ['misc', 'music', 'shoes', 'toys']:
                            print('product!!!')
                            try:
                                image_path = os.path.join('images', category_name, product_name)
                                print('product things')
                                product = Product(name=product_name_no_ext, price=randint(49,99), description=descriptions_things[randint(0,6)], image=image_path, quantity=randint(5,10), category_id=category.id)
                                db.session.add(product)
                                db.session.commit()
                            except Exception as e:
                                print(f"Error while adding product {product_name_no_ext}: {e}")
                                db.session.rollback()         


            admin = User(name='admin', email='admin@shrek.com', password='abc123', admin=True)
            db.session.add(admin)
            db.session.commit()

            print('Default entries added successfully')
        
        except Exception as e:
            print('Didnt work', e)

create_tables()


'''====== Get prodcuts to display at new arrivals ====='''
def get_new_arrivals():
    products = Product.query.order_by(Product.id.desc()).limit(10).all()
    return products

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
    new_arrivals = get_new_arrivals()
    return render_template("homepage.html", new_arrivals=new_arrivals)

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

''' ========== CART PAGES ========== '''
'''Return the cart page'''
@app.route('/cart')
def Cart():
    if 'logged_in' not in session:
        return make_response(jsonify({'message': 'Please log in to view cart'}), 401)
    user = User.query.filter_by(id=session['user_id']).first()
    order = Order.query.filter_by(user_id=session['user_id']).first()
    return render_template("cart.html", user = user, order = order)

'''Delete a cart item'''
@app.route('/delete_orderItem/<order>/<id>', methods=['GET', 'POST'])
def delete_orderItem(order, id):
    item = Order_item.query.filter_by(order_id=order, id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('Cart'))

''' ========== PAYMENT PAGES =========='''
'''Calls "Create_CompletedOrder" and if successful returns the payment page'''
@app.route('/payment/<id>/<price>', methods=['POST'])
def Payment(id, price):
    if 'logged_in' not in session:
        return make_response(jsonify({'message': 'Please log in to view account'}), 401)
    session['order_id'] = id
    user = User.query.filter_by(id=session['user_id']).first()
    order = Order.query.filter_by(user_id=session['user_id']).first()
    return(Create_CompletedOrder(user, order, price))
#    return render_template("payment.html", user = user, order = order, orderPrice = price)

'''
= takes order item from cart and adds to compled order = 
'''
@app.route('/create_CompletedOrder/<in_user>/<in_order>/<orderPrice>', methods=['POST'])
def Create_CompletedOrder(in_user, in_order, orderPrice):
    try:
        user_id = session['user_id']
        TheOrder = Order.query.filter_by(user_id=user_id).first()
        order_id = TheOrder.id
        itemsInOrder = Order_item.query.filter_by(order_id=order_id).all()
        
        if not itemsInOrder or not TheOrder:
            return make_response(jsonify({'message': 'Missing order items or user'}), 500)
        try:
            #removes uncompleted orders
            old_Orders = Completed_orders.query.filter_by(user_id=user_id, the_status=False).all()
            if old_Orders:
                for everyorder in old_Orders:
                    old_itemsInOrder = Completed_order_item.query.filter_by(order_id=order_id).all()
                    db.session.delete(everyorder)
                    for everyitem in old_itemsInOrder:
                        db.session.delete(everyitem)
                db.session.commit()
        except Exception as e:
            return make_response(jsonify({'message': 'could not remove old orders'}), 500)
        
        new_order = Completed_orders(user_id=user_id, shipping_address=' ', shipping_country=' ', the_status=False)
        #new_order = Order(user_id=user_id)
        db.session.add(new_order)

        for orderItem in itemsInOrder:
            price = Product.query.filter_by(id=orderItem.product_id).first().price
            order_item = Completed_order_item(product_id=orderItem.product_id, quantity=orderItem.quantity, price=price, order_id=new_order.id)
            db.session.add(order_item)
        
        db.session.commit()
        order_items = Completed_order_item.query.filter_by(order_id=new_order.id).all()

        total_price = 0
        for item in order_items:
            total_price += item.price*item.quantity
        
        if str(total_price) == orderPrice:
            db.session.commit()
            return render_template("payment.html", user = in_user, prosses_order = new_order, orderPrice = orderPrice)
        else:
            '''
            printing = [
                {
                    "id": item.id,
                    "price": item.price,
                    # Add more fields as needed
                }
                for item in order_items
            ]
            '''
            return make_response(jsonify({'message': 'Could not complete order due to price mismatch, try again'}), 401)

    except Exception as e:
        return make_response(jsonify({'message': 'Error: ' + str(e)}), 500)

'''add shipping and redirect'''
@app.route('/add_shipping/<order_id>/<country>/<address>', methods=['POST'])
def Add_shipping(order_id, country, address):
    try:
        TheOrder = Completed_orders.query.filter_by(id=order_id).first()
        TheOrder.shipping_country = country
        TheOrder.shipping_address = address
        return Complete_order(order_id)
    except Exception as e:
        return make_response(jsonify({'message': 'Could not add shipping'}), 401)

'''Completes the order page'''
@app.route('/complete_order/<order_id>', methods=['POST', 'GET'])
def Complete_order(order_id):
    if 'logged_in' not in session:
        return make_response(jsonify({'message': 'Please log in to view cart'}), 401)
    try: 
        Completed_orders.query.filter_by(id=order_id).first().the_status = True
    except Exception as e:
        return make_response(jsonify({'message': 'Could not complete order, status remain false'}), 401)
    try:
        #removes from "cart"
        user_id = session['user_id']
        TheOrder = Order.query.filter_by(user_id=user_id).first()
        itemsInOrder = Order_item.query.filter_by(order_id=order_id).all()
        db.session.delete(TheOrder)
        for everyitem in itemsInOrder:
            db.session.delete(everyitem)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'message': 'Could not complete order'}), 401)
    
    user = User.query.filter_by(id=session['user_id']).first()
    return redirect(url_for('Completed_order_page', user_id= user.id, order_id=order_id))

'''Return the completed order page'''
@app.route('/completed_order_page/<user_id>/<order_id>', methods=['POST', 'GET'])
def Completed_order_page(user_id,order_id):
    if 'logged_in' not in session:
        return make_response(jsonify({'message': 'Please log in to view cart'}), 401)    
    user = User.query.filter_by(id=session['user_id']).first()
    order = Completed_orders.query.filter_by(user_id=session['user_id'], id=order_id).first()
    return render_template("completed_order.html", user = user, order = order)

'''Return complete order items for a specific order'''
@app.route('/Get_complete_order_items/<int:id>', methods=['GET'])
def get_complete_order_items(id) -> str:
    try:
        order_items = Completed_order_item.query.filter_by(order_id=id).all()
        return make_response(jsonify({'order_items': [order_item.json() for order_item in order_items]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting order items', 'error': str(e)}), 500)

'''========================================='''
'''
= Return the specific category Page =
category_name: name of the category
'''
@app.route('/categories/<category_name>', methods=['GET'])
def Specific_category(category_name) -> str:
    # get category from the database
    try:
        category = Category.query.filter(Category.category_name.ilike(category_name)).first()
        if category is None:
            return "Category not found"
        products = Product.query.filter_by(category_id=category.id).all()
        return render_template("show_category.html", category=category, products=products)
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
                session['admin'] = user.admin
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

            session['logged_in'] = True
            session['user_id'] = user.id
            session['username'] = user.name
            session['admin'] = user.admin

            flash('Successfully registered', 'success')
            return redirect(url_for('Home'))  # Redirect to the login page

    else:
        return render_template("register.html")

'''Return your account page'''
@app.route('/myaccount')
def MyAccount():
    '''
    #orders = db.session.query(Order, User).join(User, Order.user_id == User.id).all()
    #user = User.query.all()
    if 'logged_in' not in session:
        return make_response(jsonify({'message': 'Please log in to view account'}), 401)
    product = Product.query.all()
    user = User.query.filter_by(id=session['user_id']).all()
    orders = db.session.query(Order, User).join(User).filter(User.id == session['user_id']).all()
    #orders = Completed_orders.query.filter_by(user_id=session['user_id']).all()
    return render_template("account.html", user = user, users = user, orders = orders, products=product)'''
    orders = db.session.query(Completed_orders, User).join(User, Completed_orders.user_id == User.id).filter(User.id == session['user_id'], Completed_orders.the_status == True).all()
    product = Product.query.all()
    users = User.query.all()
    user = User.query.filter_by(id=session['user_id']).all()
    if not session.get('logged_in'):
        return redirect(url_for('Home'))
    else:
        return render_template('account.html', users=users, products=product, orders=orders, user=user)

'''    
    orders = db.session.query(Order, User).join(User, Order.user_id == User.id).all()
    product = Product.query.all()
    user = User.query.all()
    if not session.get('logged_in') or not session.get('admin'):
        return redirect(url_for('Home'))
    else:
        return render_template('admin.html', users=user, products=product, orders=orders)
'''

'''Return order items for a specific order'''
@app.route('/order_items/<int:id>', methods=['GET'])
def get_order_items(id) -> str:
    try:
        order_items = Order_item.query.filter_by(order_id=id).all()
        return make_response(jsonify({'order_items': [order_item.json() for order_item in order_items]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting order items', 'error': str(e)}), 500)

'''Return all completed order ids of a user''' 
@app.route('/all_orders/<int:user_id>', methods=['GET'])
def get_all_order_items(user_id) -> str:
    try:
        order_id = Completed_orders.query.filter_by(user_id=user_id).all()
        return make_response(jsonify({'orders': [order_id.json() for order_id in order_id]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting order items', 'error': str(e)}), 500)

'''Return product from product_id'''
@app.route('/get_product/<int:id>', methods=['GET'])
def get_product(id) -> str:
    try:
        product = Product.query.filter_by(id=id).first()
        return make_response(jsonify({'product': product.json()}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting product', 'error': str(e)}), 500)

'''Update user creadentials'''
@app.route('/update_user', methods=['PUT'])
def update_user() -> str:
    try:
        if 'logged_in' not in session:
            return make_response(jsonify({'message': 'Please log in to update user'}), 401)
        request.get_json()
        user = User.query.filter_by(id=session['user_id']).first()
        user.name = request.json.get('name')
        session['username'] = user.name
        db.session.commit()
        return make_response(jsonify({'message': 'Successfully updated user'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating user', 'error': str(e)}), 500)
    
'''Return order size for a specific order'''
@app.route('/order_size', methods=['GET'])
def order_size() -> str:
    try:
        if 'logged_in' not in session:
            return make_response(jsonify({'message': 'Please log in to view order size', 'LoggedIn': False}), 200)
        order = Order.query.filter_by(user_id=session['user_id']).first()
        if order is None:
            return make_response(jsonify({'order_size': 0, 'LoggedIn': True}), 200)
        order_items = Order_item.query.filter_by(order_id=order.id).all()
        return make_response(jsonify({'order_size': len(order_items), 'LoggedIn': True}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting order size', 'error': str(e)}), 500)
    
'''Return order total'''
@app.route('/order_total', methods=['GET'])
def order_total() -> str:
    try:
        if 'logged_in' not in session:
            return make_response(jsonify({'message': 'Please log in to view order total'}), 401)
        order = Order.query.filter_by(user_id=session['user_id']).first()
        if order is None:
            return make_response(jsonify({'order_total': 0}), 200)
        order_items = Order_item.query.filter_by(order_id=order.id).all()
        total = sum(order_item.product.price * order_item.quantity for order_item in order_items)
        return make_response(jsonify({'order_total': total}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting order total', 'error': str(e)}), 500)

'''Return order total'''
@app.route('/compledorder_total/<order_id>', methods=['GET'])
def compledorder_total(order_id) -> str:
    try:
        if 'logged_in' not in session:
            return make_response(jsonify({'message': 'Please log in to view order total'}), 401)
        order = Completed_orders.query.filter_by(user_id=session['user_id'], id=order_id).first()
        if order is None:
            return make_response(jsonify({'order_total': 0}), 200)
        order_items = Completed_order_item.query.filter_by(order_id=order.id).all()
        total = sum(order_item.product.price * order_item.quantity for order_item in order_items)
        return make_response(jsonify({'order_total': total}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting order total', 'error': str(e)}), 500)
    
'''Return the checkout page'''
@app.route('/checkout')
def Checkout():
    return 'Checkout Page'

'''Return the admin page'''
@app.route('/admin_console')
def Admin():
    orders = db.session.query(Completed_orders, User).join(User, Completed_orders.user_id == User.id).all()
    product = Product.query.all()
    user = User.query.all()
    if not session.get('logged_in') or not session.get('admin'):
        return redirect(url_for('Home'))
    else:
        return render_template('admin.html', users=user, products=product, orders=orders)

''' Update the price of a product '''
@app.route('/update_price/<int:product_id>', methods=['PUT'])
def update_price(product_id):
    # Get the new price from the request data
    data = request.get_json()
    new_price = data['price']

    # Find the product and update its price
    product = Product.query.get(product_id)
    if product:
        product.price = new_price
        db.session.commit()
        return jsonify(success=True), 200
    else:
        return jsonify(success=False, error='Product not found'), 404

'''Create a new product and add to the database'''
@app.route('/create_product', methods=['POST'])
def create_product():
    name = request.form.get('product_name')
    price = request.form.get('product_price')
    description = request.form.get('product_description')
    image = request.files.get('product_image')
    quantity = request.form.get('product_quantity')
    category_name = request.form.get('product_category')

    # Get the category based on the name
    category = Category.query.filter_by(category_name=category_name).first()

    if category:
        category_id = str(category.id)  # Convert category_id to string
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.abspath(os.path.join('static/images', category_id, filename))
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            image_url = os.path.join('images', category_id, filename)

            # Create the Product object after obtaining the image URL
            product = Product(name=name, price=price, description=description, image=image_url, quantity=quantity, category_id=category_id)

            # Save the Product object to the database
            db.session.add(product)
            db.session.commit()

            return jsonify({'success': True})
        else:
            # Handle the case where no image is uploaded
            return jsonify({'success': False, 'error': 'No image uploaded'}), 400
    else:
        # Handle the case where the category is not found
        return jsonify({'success': False, 'error': 'Category not found'}), 400

'''Delete a product from the database'''
@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return jsonify({'success': True})

'''Update the quantity of a product'''
@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    product_id = request.json.get('product_id')
    change = int(request.json.get('change'))
    product = Product.query.get(product_id)
    if product:
        # Update the quantity of the product
        if product.quantity + change < 0:
            return jsonify({'success': False, 'error': 'Quantity cannot be less than 0'})
        
        product.quantity += change

        # Save the changes to the database
        db.session.commit()    
    return jsonify({'success': True})

'''Delete a user'''
@app.route('/delete_order/<id>', methods=['POST'])
def delete_order(id):
    order = Completed_orders.query.get(id)
    if order:
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for('Admin')) 

'''Delete a user'''
@app.route('/delete_user/<id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('Admin')) 

'''Logout the user'''
@app.route('/logout', methods=['GET'])
def Logout():
    try:
        session.clear()
        return make_response(jsonify({'message': 'Successfully logged out'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error logging out', 'error': str(e)}), 500)
    
'''Return login status'''
@app.route('/login_status', methods=['GET'])
def login_status():
    if 'logged_in' in session:
        return make_response(jsonify({'logged_in': True}), 200)
    else:
        return make_response(jsonify({'message': 'Please log in before accessing the resource.'}), 401)
    
'''get user role'''
@app.route('/get_user_role', methods=['GET'])
def get_user_role():
    if 'logged_in' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return make_response(jsonify({'role': user.admin}), 200)
    else:
        return make_response(jsonify({'role': None}), 200)
    

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
        if 'logged_in' in session:
            request.get_json()
            user_id = session['user_id']
            rating = request.json.get('rating')
            comment = request.json.get('comment')
            review = Review(product_id=id, user_id=user_id, rating=rating, comment=comment)
            db.session.add(review)
            db.session.commit()
            return make_response(jsonify({'message': 'Successfully posted review'}), 200)
        return make_response(jsonify({'message': 'Please log in to post review'}), 401)
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
            return render_template("search_results.html", products=products, search_term=search_term)
        return render_template("search_results.html", products=None, search_term=search_term)
    except Exception as e:
        return make_response(jsonify({'message': 'error searching', 'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)