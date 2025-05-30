import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_item():
    response = client.post(
        "/items",
        json={"name": "Test Item", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404

def test_update_item():
    # Create first
    create_response = client.post(
        "/items",
        json={"name": "Original", "description": "Original desc"}
    )
    item_id = create_response.json()["id"]
    
    # Update
    response = client.put(
        f"/items/{item_id}",
        json={"name": "Updated", "description": "Updated desc"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"

def test_delete_item():
    # Create first
    create_response = client.post(
        "/items",
        json={"name": "To Delete", "description": "Delete me"}
    )
    item_id = create_response.json()["id"]
    
    # Delete
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    
    # Verify deleted
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
