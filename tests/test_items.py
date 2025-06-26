def test_read_items(client):
    response = client.get("/api/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["title"] == "Test Item"
    assert data[0]["description"] == "Test item description"
    assert data[0]["price"] == 99.99

def test_read_item(client):
    response = client.get("/api/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "Test item description"
    assert data["price"] == 99.99
    assert len(data["categories"]) > 0
    assert data["categories"][0]["title"] == "Test Category"

def test_read_item_not_found(client):
    response = client.get("/api/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_create_item(client):
    item_data = {
        "title": "New Item",
        "description": "New item description",
        "price": 149.99,
        "category_ids": [1, 2]
    }
    response = client.post("/api/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Item"
    assert data["description"] == "New item description"
    assert data["price"] == 149.99
    assert "id" in data
    assert len(data["categories"]) == 2

def test_create_item_no_categories(client):
    item_data = {
        "title": "No Category Item",
        "description": "Item without categories",
        "price": 29.99,
        "category_ids": []
    }
    response = client.post("/api/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "No Category Item"
    assert data["description"] == "Item without categories"
    assert data["price"] == 29.99
    assert "id" in data
    assert len(data["categories"]) == 0

def test_update_item(client):
    item_data = {
        "title": "Updated Item",
        "description": "Updated item description",
        "price": 199.99,
        "category_ids": [2]
    }
    response = client.put("/api/items/1", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Item"
    assert data["description"] == "Updated item description"
    assert data["price"] == 199.99
    assert data["id"] == 1
    assert len(data["categories"]) == 1
    assert data["categories"][0]["id"] == 2

def test_update_item_not_found(client):
    item_data = {
        "title": "Updated Item",
        "description": "Updated item description",
        "price": 199.99,
        "category_ids": [1]
    }
    response = client.put("/api/items/999", json=item_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_delete_item(client):
    response = client.delete("/api/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # Verify the item is deleted
    response = client.get("/api/items/1")
    assert response.status_code == 404

def test_delete_item_not_found(client):
    response = client.delete("/api/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"