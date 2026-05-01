from fastapi import FastAPI
from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    


app = FastAPI()


@app.get("/products")
def get_products():
    return[
        {"id": 1, "name": "Ноутбук", "price": 50000},
        {"id": 2, "name": " Мышь", "price": 1500}
    ]
    
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return{"id": product_id, "name": "Ноутбук", "price": 50000}



@app.post("/orders")
def create_order(order: OrderCreate):
    return {
        "id":1,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "message": "Заказ создан"
    }