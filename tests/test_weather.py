def mock_weather_response(location: str):
    return {
        "name": location,
        "main": {
            "temp": 22.5,
            "feels_like": 23.0,
            "humidity": 60,
        },
        "weather": [
            {
                "main": "Clouds",
                "description": "scattered clouds",
            }
        ],
        "wind": {
            "speed": 4.2,
        },
    }


def get_auth_headers(client, email: str, username: str):
    client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "test1234",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "test1234",
        },
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def create_weather_record(client, headers, location: str):
    return client.post(
        "/weather/current",
        json={"location": location},
        headers=headers,
    )


def test_current_weather_endpoint(client, monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.weather.fetch_current_weather",
        mock_weather_response,
    )

    headers = get_auth_headers(
        client,
        "weather@test.com",
        "weatheruser",
    )

    response = create_weather_record(
        client,
        headers,
        "Buenos Aires",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["location_query"] == "Buenos Aires"
    assert data["resolved_location"] == "Buenos Aires"
    assert data["temperature"] == 22.5
    assert data["feels_like"] == 23.0
    assert data["humidity"] == 60
    assert data["weather_main"] == "Clouds"
    assert data["weather_description"] == "scattered clouds"
    assert data["wind_speed"] == 4.2


def test_get_weather_history(client, monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.weather.fetch_current_weather",
        mock_weather_response,
    )

    headers = get_auth_headers(
        client,
        "history@test.com",
        "historyuser",
    )

    create_weather_record(
        client,
        headers,
        "Buenos Aires",
    )

    create_weather_record(
        client,
        headers,
        "Paris",
    )

    response = client.get(
        "/weather/history",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["query"] == "Paris"
    assert data[1]["query"] == "Buenos Aires"
    assert data[0]["weather_record_id"] is not None
    assert "created_at" in data[0]


def test_get_weather_records(client, monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.weather.fetch_current_weather",
        mock_weather_response,
    )

    headers = get_auth_headers(
        client,
        "records@test.com",
        "recordsuser",
    )

    create_weather_record(
        client,
        headers,
        "Buenos Aires",
    )

    create_weather_record(
        client,
        headers,
        "Paris",
    )

    response = client.get(
        "/weather/records",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["location_query"] == "Paris"
    assert data[1]["location_query"] == "Buenos Aires"


def test_get_single_weather_record(client, monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.weather.fetch_current_weather",
        mock_weather_response,
    )

    headers = get_auth_headers(
        client,
        "single@test.com",
        "singleuser",
    )

    create_response = create_weather_record(
        client,
        headers,
        "Buenos Aires",
    )

    weather_id = create_response.json()["id"]

    response = client.get(
        f"/weather/{weather_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == weather_id
    assert data["location_query"] == "Buenos Aires"


def test_update_weather_record(client, monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.weather.fetch_current_weather",
        mock_weather_response,
    )

    headers = get_auth_headers(
        client,
        "update@test.com",
        "updateuser",
    )

    create_response = create_weather_record(
        client,
        headers,
        "Buenos Aires",
    )

    weather_id = create_response.json()["id"]

    response = client.put(
        f"/weather/{weather_id}",
        json={
            "location_query": "CABA",
            "resolved_location": "Ciudad Autónoma de Buenos Aires",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == weather_id
    assert data["location_query"] == "CABA"
    assert data["resolved_location"] == "Ciudad Autónoma de Buenos Aires"


def test_delete_weather_record(client, monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.weather.fetch_current_weather",
        mock_weather_response,
    )

    headers = get_auth_headers(
        client,
        "delete@test.com",
        "deleteuser",
    )

    create_response = create_weather_record(
        client,
        headers,
        "Buenos Aires",
    )

    weather_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/weather/{weather_id}",
        headers=headers,
    )

    assert delete_response.status_code == 200
    assert (
        delete_response.json()["message"]
        == "Weather record deleted successfully"
    )

    get_response = client.get(
        f"/weather/{weather_id}",
        headers=headers,
    )

    assert get_response.status_code == 404