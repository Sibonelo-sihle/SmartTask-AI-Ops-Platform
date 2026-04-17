import pytest
from app import create_app

def test_app_creation():
    app = create_app()
    assert app is not None

def test_health_endpoint():
    app = create_app()
    client = app.test_client()
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_home_endpoint():
    app = create_app()
    client = app.test_client()
    
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json

def test_create_task():
    app = create_app()
    client = app.test_client()
    
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "This is a test",
        "deadline": "2024-12-31T23:59:59",
        "status": "pending"
    })
    
    assert response.status_code == 201
    data = response.json
    assert data["title"] == "Test Task"

def test_get_tasks():
    app = create_app()
    client = app.test_client()
    
    # Create a task first
    client.post("/tasks", json={
        "title": "Another Task",
        "description": "Test description",
        "deadline": "2024-12-31T23:59:59",
        "status": "pending"
    })
    
    # Get all tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json, list)