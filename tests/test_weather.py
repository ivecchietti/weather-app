def test_current_weather_endpoint(client, monkeypatch):
    def mock_fetch_current_weather(location: str):
        return {
            "name": "Buenos Aires",
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

    monkeypatch.setattr(
        "app.api.routes.weather.fetch_current_weather",
        mock_fetch_current_weather,
    )

    client.post(
        "/auth/register",
        json={
            "email": "weather@test.com",
            "username": "weatheruser",
            "password": "test1234",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "weather@test.com",
            "password": "test1234",
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/weather/current",
        json={"location": "Buenos Aires"},
        headers={
            "Authorization": f"Bearer {token}"
        },
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
    def mock_fetch_current_weather(location: str):
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

    monkeypatch.setattr(
        "app.api.routes.weather.fetch_current_weather",
        mock_fetch_current_weather,
    )

    client.post(
        "/auth/register",
        json={
            "email": "history@test.com",
            "username": "historyuser",
            "password": "test1234",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "history@test.com",
            "password": "test1234",
        },
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    client.post(
        "/weather/current",
        json={"location": "Buenos Aires"},
        headers=headers,
    )

    client.post(
        "/weather/current",
        json={"location": "Paris"},
        headers=headers,
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