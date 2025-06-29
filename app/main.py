from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from . import models, database, crud, schemas
from .routers import customers, categories, items, orders
from .database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize test data on startup
    db = next(database.get_db())
    
    # Check if we already have data
    if not db.query(models.Customer).first():
        # Create test customers
        customer1 = crud.create_customer(db, schemas.CustomerCreate(
            name="John", 
            surname="Doe", 
            email="john.doe@example.com"
        ))
        
        customer2 = crud.create_customer(db, schemas.CustomerCreate(
            name="Jane", 
            surname="Smith", 
            email="jane.smith@example.com"
        ))
        
        # Create categories
        electronics = crud.create_category(db, schemas.ShopItemCategoryCreate(
            title="Electronics",
            description="Electronic devices and gadgets"
        ))
        
        books = crud.create_category(db, schemas.ShopItemCategoryCreate(
            title="Books",
            description="Books, e-books, and audiobooks"
        ))
        
        # Create shop items
        laptop = crud.create_item(db, schemas.ShopItemCreate(
            title="Laptop",
            description="High-performance laptop",
            price=1200.00,
            category_ids=[electronics.id]
        ))
        
        smartphone = crud.create_item(db, schemas.ShopItemCreate(
            title="Smartphone",
            description="Latest smartphone model",
            price=800.00,
            category_ids=[electronics.id]
        ))
        
        novel = crud.create_item(db, schemas.ShopItemCreate(
            title="Novel",
            description="Bestselling fiction novel",
            price=15.99,
            category_ids=[books.id]
        ))
        
        # Create orders
        crud.create_order(db, schemas.OrderCreate(
            customer_id=customer1.id,
            items=[
                schemas.OrderItemCreate(item_id=laptop.id, quantity=1),
                schemas.OrderItemCreate(item_id=novel.id, quantity=2)
            ]
        ))
        
        crud.create_order(db, schemas.OrderCreate(
            customer_id=customer2.id,
            items=[
                schemas.OrderItemCreate(item_id=smartphone.id, quantity=1)
            ]
        ))
    
    yield
    # Cleanup code could go here if needed

app = FastAPI(title="Shop API", lifespan=lifespan)

# Include routers
app.include_router(customers.router)
app.include_router(categories.router)
app.include_router(items.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shop API"}