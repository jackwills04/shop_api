from fastapi.testclient import TestClient
import pytest

def test_create_customer(client):
    response = client.post(
        "/customers/",
        json={"name": "Test", "surname": "User", "email": "test.user@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"
    assert data["surname"] == "User"
    assert data["email"] == "test.user@example.com"
    assert "id" in data
    
    # Check that we can get the customer
    customer_id = data["id"]
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json() == data

def test_get_non_existent_customer(client):
    response = client.get("/customers/999")
    assert response.status_code == 404
    
def test_update_customer(client):
    # First create a customer
    response = client.post(
        "/customers/",
        json={"name": "Original", "surname": "Name", "email": "original@example.com"}
    )
    customer_id = response.json()["id"]
    
    # Then update it
    response = client.put(
        f"/customers/{customer_id}",
        json={"name": "Updated", "surname": "Name", "email": "updated@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["email"] == "updated@example.com"
    
def test_delete_customer(client):
    # First create a customer
    response = client.post(
        "/customers/",
        json={"name": "Delete", "surname": "Me", "email": "delete@example.com"}
    )
    customer_id = response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404