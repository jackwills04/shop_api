from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    surname: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Category schemas
class ShopItemCategoryBase(BaseModel):
    title: str
    description: Optional[str] = None

class ShopItemCategoryCreate(ShopItemCategoryBase):
    pass

class ShopItemCategory(ShopItemCategoryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# ShopItem schemas
class ShopItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float

class ShopItemCreate(ShopItemBase):
    category_ids: List[int]

class ShopItem(ShopItemBase):
    id: int
    categories: List[ShopItemCategory] = []
    
    model_config = ConfigDict(from_attributes=True)

# OrderItem schemas
class OrderItemBase(BaseModel):
    item_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    item: ShopItem
    
    model_config = ConfigDict(from_attributes=True)

# Order schemas
class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    customer: Customer
    items: List[OrderItem] = []
    
    model_config = ConfigDict(from_attributes=True)