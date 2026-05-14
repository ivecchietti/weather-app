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

    response = client.post(
        "/weather/current",
        json={"location": "Buenos Aires"},
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