import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.init_db import init_db

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    # Drop all tables after the test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Initialize test data
    init_test_data(db)

    # Create a test client
    with TestClient(app) as c:
        yield c

    # Remove the override after the test
    app.dependency_overrides.clear()

def init_test_data(db):
    """Initialize test data for the test database"""
    from app import models

    # Add customers
    customer1 = models.Customer(name="Test", surname="User", email="test.user@example.com")
    customer2 = models.Customer(name="Another", surname="User", email="another.user@example.com")
    db.add(customer1)
    db.add(customer2)
    db.flush()

    # Add categories
    category1 = models.ShopItemCategory(title="Test Category", description="Test description")
    category2 = models.ShopItemCategory(title="Another Category", description="Another description")
    db.add(category1)
    db.add(category2)
    db.flush()

    # Add shop items
    item1 = models.ShopItem(title="Test Item", description="Test item description", price=99.99)
    item1.categories = [category1]

    item2 = models.ShopItem(title="Another Item", description="Another item description", price=49.99)
    item2.categories = [category2]

    db.add(item1)
    db.add(item2)
    db.flush()

    # Add orders
    order1 = models.Order(customer_id=customer1.id)
    db.add(order1)
    db.flush()

    # Add order items
    order_item1 = models.OrderItem(shop_item_id=item1.id, quantity=2, order_id=order1.id)
    db.add(order_item1)

    db.commit()