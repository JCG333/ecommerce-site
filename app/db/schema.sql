-- Table that stores the user information
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    email VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    admin BOOLEAN
);

-- Table that stores the category information
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(32) NOT NULL,
    parent_category_id INTEGER REFERENCES category(id)
);

-- Table that stores the product information
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    price FLOAT NOT NULL,
    description VARCHAR(64),
    image VARCHAR(64),
    quantity INTEGER,
    category_id INTEGER REFERENCES category(id)
);

-- Table that stores the review information
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    rating INTEGER NOT NULL,
    comment VARCHAR(256),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Table that stores the order information
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_address VARCHAR(64) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL
);

-- Table that stores the order item information
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) NOT NULL,
    order_id INTEGER REFERENCES orders(id) NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
