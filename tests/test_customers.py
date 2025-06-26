def test_read_customers(client):
    response = client.get("/api/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["name"] == "Test"
    assert data[0]["surname"] == "User"
    assert data[0]["email"] == "test.user@example.com"

def test_read_customer(client):
    response = client.get("/api/customers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"
    assert data["surname"] == "User"
    assert data["email"] == "test.user@example.com"

def test_read_customer_not_found(client):
    response = client.get("/api/customers/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"

def test_create_customer(client):
    customer_data = {
        "name": "New",
        "surname": "Customer",
        "email": "new.customer@example.com"
    }
    response = client.post("/api/customers/", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New"
    assert data["surname"] == "Customer"
    assert data["email"] == "new.customer@example.com"
    assert "id" in data

def test_create_customer_duplicate_email(client):
    customer_data = {
        "name": "Duplicate",
        "surname": "Email",
        "email": "test.user@example.com"  # This email already exists
    }
    response = client.post("/api/customers/", json=customer_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_update_customer(client):
    customer_data = {
        "name": "Updated",
        "surname": "User",
        "email": "updated.user@example.com"
    }
    response = client.put("/api/customers/1", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["surname"] == "User"
    assert data["email"] == "updated.user@example.com"
    assert data["id"] == 1

def test_update_customer_not_found(client):
    customer_data = {
        "name": "Updated",
        "surname": "User",
        "email": "updated.user@example.com"
    }
    response = client.put("/api/customers/999", json=customer_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"

def test_delete_customer(client):
    response = client.delete("/api/customers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # Verify the customer is deleted
    response = client.get("/api/customers/1")
    assert response.status_code == 404

def test_delete_customer_not_found(client):
    response = client.delete("/api/customers/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"