import os
import psycopg2

from database import queries

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sfmshop",
            user="postgres",
            password="bdokean123"
        )
        return conn
    except Exception as e:
        print("Ошибка подключения к бд:", e)
        return None



def create_user(conn, name, email):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                Insert into users (name, email)
                values (%s, %s)
                returning id, name, email
                """,
                (name, email)
            )
            user = cursor.fetchone()
            
        conn.commit()
        
        return{
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }
    
    except Exception as e:
        conn.rollback()
        print("Ошибка при создании пользователя:", e)
        return None
    
    
    
def get_user_by_id(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "select id, name, email from users where id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
            
        if user is None:
            return None
        
        return{
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }
    except Exception as e:
        print("Ошибка при получении пользователя", e)
        return None
    
    
    
    
def create_order(conn, user_id, total):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                insert into orders (user_id, total)
                values (%s, %s)
                returning id, user_id, total
                """,
                (user_id, total)
            )
            order = cursor.fetchone()
            
        conn.commit()
        return{
            "id": order[0],
            "user_id": order[1],
            "total": order[2]
        }
    
    except Exception as e:
        conn.rollback()
        print("Ошибка при создании заказа:", e)
        return None
        
def get_user_orders(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select id, user_id, total
                From orders
                Where user_id = %s
                Order by id
                """,
                (user_id,)
            )
            orders = cursor.fetchall()
            
        result = []
        for order in orders:
            result.append({
                "id": order[0],
                "user_id": order[1],
                "total": order[2]
            })
        return result
    
    except Exception as e:
        print("ошибка при получении заказа:", e)
        return []

def delete_order(conn, order_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM orders WHERE id = %s",
                (order_id,)
            )
            deleted_count = cursor.rowcount

        conn.commit()
        return deleted_count

    except Exception as e:
        conn.rollback()
        print("Ошибка при удалении заказа:", e)
        return 0
    
def get_all_products(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, price, quantity FROM products"
        )
        return cursor.fetchall()
    






