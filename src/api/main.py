from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status
from src.models.product import Product
from src.models.order import Order

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    
class UserCreate(BaseModel):
    name: str
    email: str

app = FastAPI()

products = [
        {"id": 1, "name": "Ноутбук", "price": 50000},
        {"id": 2, "name": " Мышь", "price": 1500}
]



orders = []



users = [
        {"id": 1, "name": "Alex", "email": "Alex@test.ru"},
        {"id": 2, "name": "Robert", "email": "Robert@test.tu"}
    ]



@app.get("/products")
def get_products(limit: int = 10, offset: int = 0):
    try:
        products_data = get_all_products(conn)
        
        products = []
        for data in products_data:
            product = Product(data[1], data[2], data[3])  # name, price, quantity
            product.id = data[0]  # id
            products.append(product.__dict__)
        
        
        total = len(products_data)
        paginated = products[offset: offset + limit]
        return {
            "total": len(products),
            "limit": limit,
            "offset": offset,
            "products": paginated
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
        new_id = max((o["id"] for o in orders), default=0) + 1
            
        new_order = {
            "id": new_id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity
        }
        orders.append(new_order)
        return new_order
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")



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
            raise HTTPException(status_code=404, detail=f"user с id={users_id} не найден")
        return user

    except Exception:
        raise HTTPException(status_code=500, detail="Server error")





@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    try:
        new_id = max(u["id"] for u in users) + 1 if users else 1
        
        new_user = {
            "id": new_id,
            "name": user.name,
            "email": user.email
        }
        users.append(new_user)
        return new_user
    
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")