"""
Mock data simulating responses from:
1) EPEX Spot Market Data (DE Continuous)
2) A low-cost/free Weather Forecast API (inspired by Open-Meteo or similar)
"""

def get_mock_epex_spot_data():
    """
    Returns a small, mock dataset emulating EPEX Spot (DE Continuous) structure.
    This format is loosely based on typical read-only market data:
    - market name
    - a list of records for each time slot including price and volume
    """
    return {
        "market": "DE Continuous",
        "data": [
            {
                "time": "2025-01-01T00:00Z",
                "price_eur_mwh": 37.5,
                "volume_mwh": 100.2
            },
            {
                "time": "2025-01-01T01:00Z",
                "price_eur_mwh": -5.0,
                "volume_mwh": 75.1
            },
            {
                "time": "2025-01-01T02:00Z",
                "price_eur_mwh": 42.0,
                "volume_mwh": 120.0
            }
        ]
    }


def get_mock_weather_data():
    """
    Returns a small, mock dataset inspired by a typical weather forecast API
    (e.g., Open-Meteo). 
    Includes:
    - coordinates (latitude, longitude)
    - hourly forecast with time and temperature
    """
    return {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": {
            "time": [
                "2025-01-01T00:00Z",
                "2025-01-01T01:00Z",
                "2025-01-01T02:00Z"
            ],
            "temperature_2m": [2.5, 2.3, 2.1]
        }
    }
