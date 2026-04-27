from database.connection import (
    connect_to_db,
    create_user,
    get_user_by_id
)

from database.queries import (
    get_user_order_history,
    get_order_statistics,
    get_top_products
)

def main():
    conn = connect_to_db()

    if conn is None:
        return

    try:
        user = create_user(conn, "Алекс", "alex123@test.ru")
        print("Создан пользователь:", user)
        
        if user is None:
            print("Пользователь не создан")
            return

        
        found_user = get_user_by_id(conn, user["id"])
        print("Найден пользователь:", found_user)

       
        history = get_user_order_history(conn, user["id"])
        print("История заказов:")
        for item in history:
            print(item)


        stats = get_order_statistics(conn)
        print("Статистика:")
        for row in stats:
            print(row)

        
        top_products = get_top_products(conn)
        print("Топ товаров:")
        for product in top_products:
            print(product)

    finally:
        conn.close()
        
if __name__ == "__main__":
    main()