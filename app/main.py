from fastapi import FastAPI
from app.routers import customers, categories, items, orders
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop API")

# Include routers
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shop API"}