from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ShopItem)
def create_item(item: schemas.ShopItemCreate, db: Session = Depends(get_db)):
    # Create new item
    item_data = item.model_dump(exclude={"category_ids"})
    db_item = models.ShopItem(**item_data)

    # Add categories
    if item.category_ids:
        categories = db.query(models.ShopItemCategory).filter(
            models.ShopItemCategory.id.in_(item.category_ids)
        ).all()
        db_item.categories = categories

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[schemas.ShopItem])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.ShopItem).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=schemas.ShopItem)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.ShopItem)
def update_item(item_id: int, item: schemas.ShopItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update basic attributes
    item_data = item.model_dump(exclude={"category_ids"})
    for key, value in item_data.items():
        setattr(db_item, key, value)

    # Update categories
    if item.category_ids:
        categories = db.query(models.ShopItemCategory).filter(
            models.ShopItemCategory.id.in_(item.category_ids)
        ).all()
        db_item.categories = categories

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", response_model=schemas.ShopItem)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return db_item