import pytest
from agent_core.data_connectors.mock_data import (
    get_mock_epex_spot_data,
    get_mock_weather_data
)

def test_get_mock_epex_spot_data_structure():
    data = get_mock_epex_spot_data()

    # Check top-level keys
    assert "market" in data
    assert "data" in data

    # Check the type of "data"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0

    # Check a single record
    first_record = data["data"][0]
    assert "time" in first_record
    assert "price_eur_mwh" in first_record
    assert "volume_mwh" in first_record

def test_get_mock_weather_data_structure():
    weather = get_mock_weather_data()

    # Check top-level keys
    assert "latitude" in weather
    assert "longitude" in weather
    assert "hourly" in weather

    hourly = weather["hourly"]
    # Check the structure of hourly data
    assert "time" in hourly
    assert "temperature_2m" in hourly

    assert len(hourly["time"]) == len(hourly["temperature_2m"]), \
        "Number of time steps should match number of temperatures"
