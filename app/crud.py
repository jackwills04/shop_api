from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas

# Customer CRUD
def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        for key, value in customer.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

# Category CRUD
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ShopItemCategory).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()

def create_category(db: Session, category: schemas.ShopItemCategoryCreate):
    db_category = models.ShopItemCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.ShopItemCategoryCreate):
    db_category = get_category(db, category_id)
    if db_category:
        for key, value in category.model_dump().items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# ShopItem CRUD
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ShopItem).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()

def create_item(db: Session, item: schemas.ShopItemCreate):
    item_data = item.model_dump().copy()
    category_ids = item_data.pop("category_ids")
    
    db_item = models.ShopItem(**item_data)
    
    for cat_id in category_ids:
        category = get_category(db, cat_id)
        if category:
            db_item.categories.append(category)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ShopItemCreate):
    db_item = get_item(db, item_id)
    if db_item:
        item_data = item.model_dump().copy()
        category_ids = item_data.pop("category_ids")
        
        for key, value in item_data.items():
            setattr(db_item, key, value)
        
        db_item.categories.clear()
        for cat_id in category_ids:
            category = get_category(db, cat_id)
            if category:
                db_item.categories.append(category)
        
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# Order CRUD
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(customer_id=order.customer_id)
    db.add(db_order)
    db.flush()
    
    for item in order.items:
        db_order_item = models.OrderItem(**item.model_dump(), order_id=db_order.id)
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderCreate):
    db_order = get_order(db, order_id)
    if db_order:
        db_order.customer_id = order.customer_id
        
        # Remove existing items
        for item in db_order.items:
            db.delete(item)
        
        # Add new items
        for item in order.items:
            db_order_item = models.OrderItem(**item.model_dump(), order_id=db_order.id)
            db.add(db_order_item)
        
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order