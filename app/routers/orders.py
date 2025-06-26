from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Check if customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Create order
    order_data = order.model_dump(exclude={"items"})
    db_order = models.Order(**order_data)
    db.add(db_order)
    db.flush()  # Flush to get the order ID

    # Create order items
    for item in order.items:
        # Check if shop item exists
        shop_item = db.query(models.ShopItem).filter(models.ShopItem.id == item.shop_item_id).first()
        if not shop_item:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Shop item with ID {item.shop_item_id} not found")

        order_item = models.OrderItem(
            shop_item_id=item.shop_item_id,
            quantity=item.quantity,
            order_id=db_order.id
        )
        db.add(order_item)

    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Check if customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Update customer
    db_order.customer_id = order.customer_id

    # Delete existing order items
    db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()

    # Create new order items
    for item in order.items:
        # Check if shop item exists
        shop_item = db.query(models.ShopItem).filter(models.ShopItem.id == item.shop_item_id).first()
        if not shop_item:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Shop item with ID {item.shop_item_id} not found")

        order_item = models.OrderItem(
            shop_item_id=item.shop_item_id,
            quantity=item.quantity,
            order_id=db_order.id
        )
        db.add(order_item)

    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Fetch the order with all relationships before deleting
    # This ensures we have all the data needed for the response
    order_data = db.query(models.Order).options(
        joinedload(models.Order.customer),
        joinedload(models.Order.items).joinedload(models.OrderItem.shop_item)
    ).filter(models.Order.id == order_id).first()

    # Now delete the order
    db.delete(db_order)
    db.commit()

    return order_data