from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

users = [
    {'id': 1, 'name': 'Ivan Ivanov', 'email': 'i.i.ivanov@mail.com'},
    {'id': 2, 'name': 'Petr Petrov', 'email': 'p.p.petrov@mail.com'}
]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': 'nonexistent@example.com'})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    new_user = {"name": "Test User", "email": "test@example.com"}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    user_id = response.json()
    assert isinstance(user_id, int)

def test_create_user_with_invalid_email():
    duplicate_user = {"name": "Duplicate", "email": users[0]['email']}
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409

def test_delete_user():
    new_user = {"name": "ToDelete", "email": "delete@example.com"}
    post_resp = client.post("/api/v1/user", json=new_user)
    assert post_resp.status_code == 201
    del_resp = client.delete("/api/v1/user", params={'email': new_user['email']})
    assert del_resp.status_code == 204
    get_resp = client.get("/api/v1/user", params={'email': new_user['email']})
    assert get_resp.status_code == 404
