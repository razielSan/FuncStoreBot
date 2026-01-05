import pytest

from app.bot.modules.weather_forecast.childes.weather.settings import (
    settings,
    weather_translation_settings,
)
from app.bot.modules.weather_forecast.childes.weather.services.weather import (
    weather_service,
)
from app.bot.modules.weather_forecast.childes.weather.api.weather_openwm import (
    weather_openwm_api,
)
from app.core.response import NetworkResponseData


@pytest.mark.asyncio
async def test_weather_service_current_weather_success(
    monkeypatch,
    fake_logging_data,
):
    city = "test"

    fake_session = "test"

    count = 0

    async def fake_error_handlers(*args, **kwargs):
        nonlocal count
        count += 1
        if count == 1:
            return NetworkResponseData(
                message=[
                    {
                        "name": f"{city}",
                        "local_names": {
                            "ms": f"{city}",
                        },
                        "lat": 51.5073219,
                        "lon": -0.1276474,
                        "country": "GB",
                        "state": "England",
                    },
                    {"test": "Hello World"},
                ],
                error=None,
            )
        return NetworkResponseData(
            message={
                "coord": {"lon": 7.367, "lat": 45.133},
                "weather": [
                    {
                        "id": 501,
                        "main": "Rain",
                        "description": "moderate rain",
                        "icon": "10d",
                    }
                ],
                "base": "stations",
                "main": {
                    "temp": 284.2,
                    "feels_like": 282.93,
                    "temp_min": 283.06,
                    "temp_max": 286.82,
                    "pressure": 1021,
                    "humidity": 60,
                    "sea_level": 1021,
                    "grnd_level": 910,
                },
                "visibility": 10000,
                "wind": {"speed": 4.09, "deg": 121, "gust": 3.47},
                "rain": {"1h": 2.73},
                "clouds": {"all": 83},
                "dt": 1726660758,
                "sys": {
                    "type": 1,
                    "id": 6736,
                    "country": "IT",
                    "sunrise": 1726636384,
                    "sunset": 1726680975,
                },
                "timezone": 7200,
                "id": 3165523,
                "name": "Province of Turin",
                "cod": 200,
            },
            error=None,
        )

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.weather."
        "api.weather_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )

    weather_result = await weather_service.recieve(
        city=city,
        url_geolocated_openweathermap=settings.ULR_GEOLOCATED_OPENWEATHERMAP.format(
            query=city,
            appid=settings.APPID,
        ),
        logging_data=fake_logging_data,
        session=fake_session,
        url_weather=settings.URL_CURRENT_OPENWEATHERMAP,
        api_openweathermap=settings.APPID,
        weather_openwm_api=weather_openwm_api,
        weather_translation=weather_translation_settings.weather_translation,
    )
    assert weather_result.error is None
    assert isinstance(weather_result.message, str)
    assert city in weather_result.message


@pytest.mark.asyncio
async def test_weather_service_not_city_found_error(
    monkeypatch,
    fake_logging_data,
):
    city = "test"

    fake_session = "test"

    async def fake_error_handlers(*args, **kwargs):
        return NetworkResponseData(message=[], error=None)

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.weather."
        "api.weather_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )

    weather_result = await weather_service.recieve(
        city=city,
        url_geolocated_openweathermap=settings.ULR_GEOLOCATED_OPENWEATHERMAP.format(
            query=city,
            appid=settings.APPID,
        ),
        logging_data=fake_logging_data,
        session=fake_session,
        url_weather=settings.URL_CURRENT_OPENWEATHERMAP,
        api_openweathermap=settings.APPID,
        weather_openwm_api=weather_openwm_api,
        weather_translation=weather_translation_settings.weather_translation,
    )
    assert "Такого города не существует" in weather_result.error
    assert weather_result.message is None
