from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

    


app = FastAPI()

products = [
        {"id": 1, "name": "Ноутбук", "price": 50000},
        {"id": 2, "name": " Мышь", "price": 1500}
]


@app.get("/products")
def get_products(limit: int = 10, offset: int = 0):
    paginated = products[offset: offset + limit]
    
    return {
        "total": len(products),
        "limit": limit,
        "offset": offset,
        "products": paginated
    }
    
@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар с id ={product_id} не найден")
    return product

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    return {
        "id":1,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "message": "Заказ создан"
    }

users = [
        {"id": 1, "name": "Alex", "email": "Alex@test.ru"},
        {"id": 2, "name": "Robert", "email": "Robert@test.tu"}
    ]

@app.get("/users")
def get_users():
    return users
    
@app.get("/users/{users_id}", status_code=status.HTTP_200_OK)
def get_users(users_id: int):
    user = next((u for u in users if u["id"] == users_id), None)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user с id={users_id} не найден")
    return user

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(order: OrderCreate):
    return{
        "id": 1,
        "user_id": order.user_id,
        "quantity": order.quantity,
        "message": "Пользователь создан"
    }