def test_read_orders(client):
    response = client.get("/api/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "customer" in data[0]
    assert "items" in data[0]

def test_read_order(client):
    response = client.get("/api/orders/1")
    assert response.status_code == 200
    data = response.json()
    assert "customer" in data
    assert "items" in data
    assert len(data["items"]) > 0

def test_read_order_not_found(client):
    response = client.get("/api/orders/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

def test_create_order(client):
    # First, ensure we have a customer and shop item
    customer_response = client.get("/api/customers/1")
    assert customer_response.status_code == 200

    item_response = client.get("/api/items/1")
    assert item_response.status_code == 200

    order_data = {
        "customer_id": 1,
        "items": [
            {
                "shop_item_id": 1,
                "quantity": 3
            }
        ]
    }

    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 3
    assert "id" in data

def test_create_order_invalid_customer(client):
    order_data = {
        "customer_id": 999,  # Non-existent customer
        "items": [
            {
                "shop_item_id": 1,
                "quantity": 3
            }
        ]
    }

    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"

def test_create_order_invalid_item(client):
    order_data = {
        "customer_id": 1,
        "items": [
            {
                "shop_item_id": 999,  # Non-existent item
                "quantity": 3
            }
        ]
    }

    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_update_order(client):
    order_data = {
        "customer_id": 2,  # Change customer
        "items": [
            {
                "shop_item_id": 2,  # Change item
                "quantity": 5  # Change quantity
            }
        ]
    }

    response = client.put("/api/orders/1", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["shop_item_id"] == 2
    assert data["items"][0]["quantity"] == 5

def test_update_order_not_found(client):
    order_data = {
        "customer_id": 1,
        "items": [
            {
                "shop_item_id": 1,
                "quantity": 3
            }
        ]
    }

    response = client.put("/api/orders/999", json=order_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

def test_delete_order(client):
    response = client.delete("/api/orders/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # Verify the order is deleted
    response = client.get("/api/orders/1")
    assert response.status_code == 404

def test_delete_order_not_found(client):
    response = client.delete("/api/orders/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"