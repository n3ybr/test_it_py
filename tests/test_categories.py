def test_add_parent_category(auth_client):
    response = auth_client.post(
        "/categories/?name=Книги"
    )
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == 1

def test_error_add_parent_category(auth_client):
    response = auth_client.post(
        "/categories"
    )

    assert response.status_code == 422
    
def test_add_child_category(auth_client):
    response = auth_client.post(
        "/categories/?name=Романы&parent_id=0"
    )
    data = response.json()

    assert response.status_code == 200
    assert data['id'] is not None

def test_error_add_child_category(auth_client):
    response = auth_client.post(
        "/categories?name=Романы&parent_id=999"
    )

    assert response.status_code == 404

def test_get_category(auth_client):
    create_response = auth_client.post(
        "/categories/?name=Книги"
    )
    assert create_response.status_code == 200

    response = auth_client.get(
        f"/categories/1"
    )

    assert response.status_code == 200

def test_update_category(auth_client):
    create_response = auth_client.post(
        "/categories/?name=Книги"
    )
    assert create_response.status_code == 200

    response = auth_client.put(
        f"categories/1?name=Старые книги"
    )
    data = response.json()

    assert response.status_code == 200
    assert data["new_name"] == "Старые книги"

def test_delete_category(auth_client):
    create_response = auth_client.post(
        "/categories/?name=Книги"
    )
    assert create_response.status_code == 200

    response = auth_client.delete(
        f"categories/1"
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 1