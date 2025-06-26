from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ShopItemCategory)
def create_category(category: schemas.ShopItemCategoryCreate, db: Session = Depends(get_db)):
    db_category = models.ShopItemCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[schemas.ShopItemCategory])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(models.ShopItemCategory).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=schemas.ShopItemCategory)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=schemas.ShopItemCategory)
def update_category(category_id: int, category: schemas.ShopItemCategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # Update category attributes
    for key, value in category.model_dump().items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", response_model=schemas.ShopItemCategory)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return db_category