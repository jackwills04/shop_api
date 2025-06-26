# Shop API

A minimalistic backend web app for an online shop built with FastAPI.

## Features

- Full CRUD operations for Customers, Shop Item Categories, Shop Items, and Orders
- SQLite database for data persistence
- Automatic API documentation with Swagger UI
- Comprehensive test suite

## Project Structure

```
shop_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── init_db.py           # Database initialization script
│   └── routers/             # API endpoints
│       ├── __init__.py
│       ├── customers.py
│       ├── categories.py
│       ├── items.py
│       └── orders.py
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_customers.py
│   ├── test_categories.py
│   ├── test_items.py
│   └── test_orders.py
├── requirements.txt         # Project dependencies
├── run.py                   # Script to run the application
└── README.md                # Project documentation
```

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd shop_api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the application with:

```bash
python run.py
```

The API will be available at http://localhost:8000

You can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

Run the tests with:

```bash
pytest
```

For more verbose output:

```bash
pytest -v
```

## API Endpoints

### Customers

- `GET /api/customers/` - List all customers
- `GET /api/customers/{customer_id}` - Get a specific customer
- `POST /api/customers/` - Create a new customer
- `PUT /api/customers/{customer_id}` - Update a customer
- `DELETE /api/customers/{customer_id}` - Delete a customer

### Shop Item Categories

- `GET /api/categories/` - List all categories
- `GET /api/categories/{category_id}` - Get a specific category
- `POST /api/categories/` - Create a new category
- `PUT /api/categories/{category_id}` - Update a category
- `DELETE /api/categories/{category_id}` - Delete a category

### Shop Items

- `GET /api/items/` - List all items
- `GET /api/items/{item_id}` - Get a specific item
- `POST /api/items/` - Create a new item
- `PUT /api/items/{item_id}` - Update an item
- `DELETE /api/items/{item_id}` - Delete an item

### Orders

- `GET /api/orders/` - List all orders
- `GET /api/orders/{order_id}` - Get a specific order
- `POST /api/orders/` - Create a new order
- `PUT /api/orders/{order_id}` - Update an order
- `DELETE /api/orders/{order_id}` - Delete an order

## Data Models

### Customer
- ID (integer)
- Name (string)
- Surname (string)
- Email (string)

### ShopItemCategory
- ID (integer)
- Title (string)
- Description (string)

### ShopItem
- ID (integer)
- Title (string)
- Description (string)
- Price (float)
- Category (list of ShopItemCategory)

### OrderItem
- ID (integer)
- ShopItem (ShopItem)
- Quantity (integer)

### Order
- ID (integer)
- Customer (Customer)
- Items (list of OrderItem)