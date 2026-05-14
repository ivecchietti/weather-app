from uuid import uuid4


def test_register_user(client):
    unique_id = uuid4().hex

    response = client.post(
        "/auth/register",
        json={
            "email": f"testuser_{unique_id}@test.com",
            "username": f"testuser_{unique_id}",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == f"testuser_{unique_id}@test.com"
    assert data["username"] == f"testuser_{unique_id}"


def test_login_user(client):
    client.post(
        "/auth/register",
        json={
            "email": "testuser2@test.com",
            "username": "testuser2",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "testuser2@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "fake@test.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid email or password"
    }


def test_register_duplicate_user(client):
    user_data = {
        "email": "duplicate@test.com",
        "username": "duplicate",
        "password": "password123",
    }

    client.post("/auth/register", json=user_data)
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email or username already registered"
    }


def test_get_current_user_with_valid_token(client):
    user_data = {
        "email": "me@test.com",
        "username": "meuser",
        "password": "password123",
    }

    client.post("/auth/register", json=user_data)

    login_response = client.post(
        "/auth/login",
        json={
            "email": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]