import pytest

from app.bot.modules.weather_forecast.childes.aqi.services.aqi import aqi_service
from app.bot.modules.weather_forecast.childes.aqi.api.aqi_openwm import aqi_openwm_api
from app.bot.modules.weather_forecast.childes.aqi.settings import aqi_settings, settings
from app.core.response import NetworkResponseData


@pytest.mark.unit
@pytest.mark.asyncio
async def test_aqi_service_succes(
    fake_logging_data,
    monkeypatch,
):

    fake_session = "test_session"
    city = "test".title()

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
                status=200,
                error=None,
            )

        return NetworkResponseData(
            message={
                "coord": {"lon": 83.1068, "lat": 54.758},
                "list": [
                    {
                        "main": {"aqi": 2},
                        "components": {
                            "co": 174.36,
                            "no": 0.04,
                            "no2": 2.11,
                            "o3": 72.4,
                            "so2": 1.45,
                            "pm2_5": 2.66,
                            "pm10": 3.2,
                            "nh3": 0.02,
                        },
                        "dt": 1767501560,
                    }
                ],
            },
            status=200,
            error=None,
        )

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.aqi.api.aqi_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )

    result_aqi = await aqi_service.recieve(
        city=city,
        api_openweathermap=settings.APPID,
        url_air_pollution=settings.URL_AIR_POLLUTION,
        url_geolocated_openweathermap=settings.ULR_GEOLOCATED_OPENWEATHERMAP.format(
            query=city,
            appid=settings.APPID,
        ),
        air_pollution=aqi_settings.AIR_POLLUTION,
        aqi=aqi_settings.AQI,
        session=fake_session,
        logging_data=fake_logging_data,
        aqi_openwm_api=aqi_openwm_api,
    )

    assert city in result_aqi.message
    assert isinstance(result_aqi.message, str)
    assert result_aqi.error is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_aqi_service_not_found_city_error(
    fake_logging_data,
    monkeypatch,
):

    fake_session = "test_session"
    city = "test".title()

    async def fake_error_handlers(*args, **kwargs):
        return NetworkResponseData(
            message=[],
            error=None,
        )

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.aqi.api.aqi_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )

    result_aqi = await aqi_service.recieve(
        city=city,
        api_openweathermap=settings.APPID,
        url_air_pollution=settings.URL_AIR_POLLUTION,
        url_geolocated_openweathermap=settings.ULR_GEOLOCATED_OPENWEATHERMAP.format(
            query=city,
            appid=settings.APPID,
        ),
        air_pollution=aqi_settings.AIR_POLLUTION,
        aqi=aqi_settings.AQI,
        session=fake_session,
        logging_data=fake_logging_data,
        aqi_openwm_api=aqi_openwm_api,
    )

    assert "Такого города не существует" in result_aqi.error
    assert result_aqi.message is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_aqi_service_not_aqi_error(
    fake_logging_data,
    monkeypatch,
):

    fake_session = "test_session"
    city = "test".title()

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
                status=200,
                error=None,
            )
        return NetworkResponseData(
            message=[],
            error=None,
        )

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.aqi.api.aqi_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )

    result_aqi = await aqi_service.recieve(
        city=city,
        api_openweathermap=settings.APPID,
        url_air_pollution=settings.URL_AIR_POLLUTION,
        url_geolocated_openweathermap=settings.ULR_GEOLOCATED_OPENWEATHERMAP.format(
            query=city,
            appid=settings.APPID,
        ),
        air_pollution=aqi_settings.AIR_POLLUTION,
        aqi=aqi_settings.AQI,
        session=fake_session,
        logging_data=fake_logging_data,
        aqi_openwm_api=aqi_openwm_api,
    )

    assert "Нет данных о загрязнении воздуха для" in result_aqi.error
    assert result_aqi.message is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_aqi_service_geolocation_network_error(
    fake_logging_data,
    monkeypatch,
):
    fake_session = "test_session"
    city = "Test"

    async def fake_error_handlers(*args, **kwargs):
        return NetworkResponseData(
            message=None,
            error="Network error",
        )

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.aqi.api.aqi_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )

    result = await aqi_service.recieve(
        city=city,
        api_openweathermap=settings.APPID,
        url_air_pollution=settings.URL_AIR_POLLUTION,
        url_geolocated_openweathermap=settings.ULR_GEOLOCATED_OPENWEATHERMAP.format(
            query=city,
            appid=settings.APPID,
        ),
        air_pollution=aqi_settings.AIR_POLLUTION,
        aqi=aqi_settings.AQI,
        session=fake_session,
        logging_data=fake_logging_data,
        aqi_openwm_api=aqi_openwm_api,
    )

    assert result.message is None
    assert "Network error" in result.error


@pytest.mark.unit
@pytest.mark.asyncio
async def test_aqi_service_empty_components(
    fake_logging_data,
    monkeypatch,
):
    fake_session = "test_session"
    city = "Test"
    count = 0

    async def fake_error_handlers(*args, **kwargs):
        nonlocal count
        count += 1
        if count == 1:
            return NetworkResponseData(
                message=[{"name": city, "lat": 1, "lon": 1}],
                error=None,
            )
        return NetworkResponseData(
            message={
                "list": [{"main": {"aqi": 2}, "components": {}}],
            },
            error=None,
        )

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.aqi.api.aqi_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )

    result = await aqi_service.recieve(
        city=city,
        api_openweathermap=settings.APPID,
        url_air_pollution=settings.URL_AIR_POLLUTION,
        url_geolocated_openweathermap=settings.ULR_GEOLOCATED_OPENWEATHERMAP.format(
            query=city,
            appid=settings.APPID,
        ),
        air_pollution=aqi_settings.AIR_POLLUTION,
        aqi=aqi_settings.AQI,
        session=fake_session,
        logging_data=fake_logging_data,
        aqi_openwm_api=aqi_openwm_api,
    )

    assert isinstance(result.message, str)
    assert result.error is None
