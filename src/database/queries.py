import psycopg2

def get_orders_with_products(conn, user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            select
                orders.id as orders_id,
                products.name as product_name,
                products.price,
                order_items.quantity
            from orders
            join order_items on orders.id = order_items.order_id
            join products on order_items.product_id = products.id
            where orders.user_id = %s
            order by orders.id
            """,
            (user_id,)
        )
        return cursor.fetchall()


    
def get_products_sorted_by_price(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            select id, name, price, quantity
            from products
            order by price desc
            """
        )
        return cursor.fetchall()
    
def get_user_order_history(conn, user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                orders.id AS order_id,
                orders.created_at,
                products.name AS product_name,
                products.price,
                order_items.quantity
            FROM orders
            INNER JOIN order_items 
                ON orders.id = order_items.order_id
            INNER JOIN products
                ON order_items.product_id = products.id
            WHERE orders.user_id = %s
            ORDER BY orders.created_at DESC
            """,
            (user_id,)
        )
        return cursor.fetchall()
    
def get_order_statistics(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                users.id,
                users.name,
                COUNT(orders.id) AS orders_count,
                COALESCE(SUM(orders.total), 0) AS total_sum
            FROM users
            LEFT JOIN orders
                ON users.id = orders.user_id
            GROUP BY users.id, users.name
            ORDER BY total_sum DESC
            """
        )
        return cursor.fetchall()
    
    
def get_top_products(conn, limit=5):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                products.id,
                products.name,
                SUM(order_items.quantity) AS total_sold
            FROM products
            JOIN order_items 
                ON products.id = order_items.product_id
            GROUP BY products.id, products.name
            ORDER BY total_sold DESC
            LIMIT %s
            """,
            (limit,)
        )
        return cursor.fetchall()
    
