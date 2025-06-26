def test_read_categories(client):
    response = client.get("/api/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["title"] == "Test Category"
    assert data[0]["description"] == "Test description"

def test_read_category(client):
    response = client.get("/api/categories/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Category"
    assert data["description"] == "Test description"

def test_read_category_not_found(client):
    response = client.get("/api/categories/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"

def test_create_category(client):
    category_data = {
        "title": "New Category",
        "description": "New category description"
    }
    response = client.post("/api/categories/", json=category_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Category"
    assert data["description"] == "New category description"
    assert "id" in data

def test_update_category(client):
    category_data = {
        "title": "Updated Category",
        "description": "Updated category description"
    }
    response = client.put("/api/categories/1", json=category_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Category"
    assert data["description"] == "Updated category description"
    assert data["id"] == 1

def test_update_category_not_found(client):
    category_data = {
        "title": "Updated Category",
        "description": "Updated category description"
    }
    response = client.put("/api/categories/999", json=category_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"

def test_delete_category(client):
    response = client.delete("/api/categories/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # Verify the category is deleted
    response = client.get("/api/categories/1")
    assert response.status_code == 404

def test_delete_category_not_found(client):
    response = client.delete("/api/categories/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"