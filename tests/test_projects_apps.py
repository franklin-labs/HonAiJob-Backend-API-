import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.sqlalchemy_user import User
from app.core.security import create_access_token

def test_create_project(client: TestClient, db: Session, normal_user_token_headers: dict):
    data = {"name": "Test Project", "description": "Test Description"}
    response = client.post("/api/v1/projects/", json=data, headers=normal_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content

def test_read_projects(client: TestClient, db: Session, normal_user_token_headers: dict):
    response = client.get("/api/v1/projects/", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_application(client: TestClient, db: Session, normal_user_token_headers: dict):
    # Create a project first
    project_data = {"name": "App Project"}
    project_res = client.post("/api/v1/projects/", json=project_data, headers=normal_user_token_headers)
    project_id = project_res.json()["id"]
    
    app_data = {
        "company": "Test Company",
        "role": "Developer",
        "status": "in_progress",
        "project_id": project_id
    }
    response = client.post("/api/v1/applications/", json=app_data, headers=normal_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["company"] == app_data["company"]
    assert content["project_id"] == project_id
