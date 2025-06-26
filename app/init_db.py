from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal, engine

def init_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if we already have data
        if db.query(models.Customer).first():
            return

        # Add customers
        customer1 = models.Customer(name="John", surname="Doe", email="john.doe@example.com")
        customer2 = models.Customer(name="Jane", surname="Smith", email="jane.smith@example.com")
        db.add(customer1)
        db.add(customer2)
        db.flush()

        # Add categories
        category1 = models.ShopItemCategory(title="Electronics", description="Electronic devices and accessories")
        category2 = models.ShopItemCategory(title="Books", description="Physical and digital books")
        category3 = models.ShopItemCategory(title="Clothing", description="Apparel and fashion items")
        db.add(category1)
        db.add(category2)
        db.add(category3)
        db.flush()

        # Add shop items
        item1 = models.ShopItem(title="Smartphone", description="Latest model smartphone", price=999.99)
        item1.categories = [category1]

        item2 = models.ShopItem(title="Laptop", description="High-performance laptop", price=1499.99)
        item2.categories = [category1]

        item3 = models.ShopItem(title="Python Programming", description="Comprehensive guide to Python", price=39.99)
        item3.categories = [category2]

        item4 = models.ShopItem(title="T-shirt", description="Cotton t-shirt", price=19.99)
        item4.categories = [category3]

        item5 = models.ShopItem(title="Smart Watch", description="Fitness and health tracker", price=299.99)
        item5.categories = [category1, category3]  # Can belong to multiple categories

        db.add(item1)
        db.add(item2)
        db.add(item3)
        db.add(item4)
        db.add(item5)
        db.flush()

        # Add orders
        order1 = models.Order(customer_id=customer1.id)
        db.add(order1)
        db.flush()

        # Add order items
        order_item1 = models.OrderItem(shop_item_id=item1.id, quantity=1, order_id=order1.id)
        order_item2 = models.OrderItem(shop_item_id=item3.id, quantity=2, order_id=order1.id)
        db.add(order_item1)
        db.add(order_item2)

        # Add another order
        order2 = models.Order(customer_id=customer2.id)
        db.add(order2)
        db.flush()

        # Add order items
        order_item3 = models.OrderItem(shop_item_id=item2.id, quantity=1, order_id=order2.id)
        order_item4 = models.OrderItem(shop_item_id=item4.id, quantity=3, order_id=order2.id)
        db.add(order_item3)
        db.add(order_item4)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized with test data")