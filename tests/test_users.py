def test_add_user(auth_client):
    response = auth_client.post("/users/add/", json={"username": "admin", "password": "Qazwsx12"})

    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "admin"

def test_add_user_invalid(auth_client):
    response = auth_client.post("/users/add/", json={"username": "admin"})

    assert response.status_code == 400

def test_get_user(auth_client):
    add_response = auth_client.post("/users/add/", json={"username": "admin", "password": "Qazwsx12"})

    assert add_response.status_code == 200

    response = auth_client.get("/users/2")
    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "admin"

def test_update_user(auth_client):
    add_response = auth_client.post("/users/add/", json={"username": "admin", "password": "Qazwsx12"})

    assert add_response.status_code == 200

    response = auth_client.put("/users/2?new_password=Qazwsx1113")
    data = response.json()

    assert response.status_code == 200
    assert data["user_id"] == 2

def test_update_invalid_user(auth_client):
    add_response = auth_client.post("/users/add/", json={"username": "admin", "password": "Qazwsx12"})

    assert add_response.status_code == 200

    response = auth_client.put("/users/999?new_password=Qazwsx1113")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Пользователь не найден"

def test_delete_user(auth_client):
    add_response = auth_client.post("/users/add/", json={"username": "admin", "password": "Qazwsx12"})

    assert add_response.status_code == 200

    response = auth_client.delete("/users/2")

    data = response.json()

    assert response.status_code == 200
    assert data["user_id"] == 2