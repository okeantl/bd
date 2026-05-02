from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status
from src.models.product import Product
from src.models.order import Order
from src.database.connection import connect_to_db, get_all_products




class OrderCreate(BaseModel):
    user_id: int
    total: float
    
class UserCreate(BaseModel):
    name: str
    email: str

app = FastAPI()

@app.on_event("startup")
async def startup():
    global conn
    conn = connect_to_db()
    
    
@app.on_event("shutdown")
async def shutdown():
    if conn:
        conn.close()




@app.get("/products")
def get_products(limit: int = 10, offset: int = 0):
    try:
        products_data = get_all_products(conn)
        
        products = []
        for data in products_data:
            product = Product(data["name"], data["price"], data["quantity"])  # name, price, quantity
            product.id = data["id"]  # id
            products.append(product.__dict__)
        
        
        total = len(products_data)
        paginated_products  = products[offset: offset + limit]
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "products": paginated_products 
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Server eror")
    
    
    
@app.get("/products/{product_id}")
def get_product(product_id: int):
    try:
        product = next((p for p in products if p["id"] == product_id), None)
        
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    except Exception:
        raise HTTPException(status_code=500, detail="Server error")



@app.post("/orders")
def create_order(order: OrderCreate):
    try:
        user = get_user_by_id(conn, order.user_id)

        if not user:
            raise HTTPException(404, "User not found")

        return create_order(
            conn,
            order.user_id,
            order.total
        )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Server error")



@app.get("/users")
def get_users():
    try:
        return users
    
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
        
    
    
    
    
    
@app.get("/users/{users_id}", status_code=200)
def get_user(user_id: int):
    try:
        user = next((u for u in users if u["id"] == user_id), None)
        
        if user is None:
            raise HTTPException(status_code=404, detail=f"user с id={user_id} не найден")
        return user

    except Exception:
        raise HTTPException(status_code=500, detail="Server error")





@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    try:
        new_id = max(u["id"] for u in users) + 1 if users else 1
        
        if not user_exists:
            raise HTTPException(404, detail="user not found")  
        
        new_user = {
            "id": new_id,
            "name": user.name,
            "email": user.email
        }
        users.append(new_user)
        return new_user
    
      
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    
    
@app.put("/products/{product_id}")
def update_product(product_id: int, product_data: dict):
    try:
        existing = get_product_by_id(conn, product_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        name = product_datap["name"]
        price = product_data["price"]
        quantity = product_data["quantity"]
        
        update_product(conn, product_id, name, pridce, quantity)
        
        product = Product(name=name, price=price, quantity=quantity)
        product.id = product_id
        return product.to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        existing = get_product_by_id(conn, product_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        delete_product(conn, product_id)
        
        return{"message": f"Товар с ID {product_id} успешно удален"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
def test_api():
    client = TestClient(app)
    
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com"
        }
    )
    assert response.status_code == 201
    user = response.json()
    user_id = user["id"]
    print("POST /users: OK")

    
    response = client.get("/users")
    assert response.status_code == 200
    print("GET /users: OK")

    
    response = client.get("/products")
    assert response.status_code == 200
    products = response.json()["products"]

    if not products:
        print(" Нет товаров в БД — пропускаем тесты products")
        return

    product_id = products[0]["id"]
    print("GET /products: OK")

    
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    print("GET /products/{id}: OK")

    
    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated",
            "price": 999,
            "quantity": 5
        }
    )
    assert response.status_code == 200
    print("PUT /products/{id}: OK")

   
    response = client.post(
        "/orders",
        json={
            "user_id": user_id,
            "total": 1000
        }
    )
    assert response.status_code in (200, 201)
    print("POST /orders: OK")

   
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    print("DELETE /products/{id}: OK")


if __name__ == "__main__":
    test_api()