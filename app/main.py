from fastapi import FastAPI, HTTPException
from app.database import db
from app.schemas import (
    UserCreate, UserResponse,
    ProductCreate, ProductResponse
)
app = FastAPI(
    title="atlas_user_product_api"
)

@app.get("/")
def home():
    return {
        'status':'ok',
        'message': 'Project is running...'
    }



@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    existing_user = db.users.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    db.users.insert_one(user.dict())
    return user



@app.get("/users/{email}", response_model=UserResponse)
def get_user_by_email(email: str):
    user = db.users.find_one(
        {"email": email},
        {"_id": 0}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user




@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate):
    existing_product = db.products.find_one({"sku": product.sku})

    if existing_product:
        raise HTTPException(status_code=400, detail="SKU already exists")

    db.products.insert_one(product.dict())
    return product



@app.get("/products/{sku}", response_model=ProductResponse)
def get_product_by_sku(sku: str):
    product = db.products.find_one(
        {"sku": sku},
        {"_id": 0}
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

