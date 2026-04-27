DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INTEGER DEFAULT 0
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER
);

INSERT INTO users (name, email) VALUES
('Alex', 'alex@test.ru'),
('Ivan', 'ivan@test.ru'),
('Maria', 'maria@test.ru');

INSERT INTO products (name, price, quantity) VALUES
('Laptop', 50000, 10),
('Mouse', 1500, 50),
('Keyboard', 3000, 30),
('Monitor', 20000, 15),
('Headphones', 4000, 25);

INSERT INTO orders (user_id, total) VALUES
(1, 51500),
(2, 23000);

INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 2, 1),
(2, 4, 1),
(2, 5, 1);