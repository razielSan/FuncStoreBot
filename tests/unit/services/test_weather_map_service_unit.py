from pathlib import Path

import pytest

from app.bot.modules.weather_forecast.childes.weather_map.api.weather_map_openwm import (
    weather_map_openwm_api,
)
from app.bot.modules.weather_forecast.childes.weather_map.services.weather_map import (
    weather_map_service,
)
from app.bot.modules.weather_forecast.childes.weather_map.settings import settings
from app.core.response import NetworkResponseData


@pytest.mark.unit
@pytest.mark.asyncio
async def test_weather_map_succes(
    fake_logging_data,
    monkeypatch,
):

    fake_session = "test_session"
    fake_path = Path(__file__).resolve()

    async def fake_error_handlers(*args, **kwargs):
        return NetworkResponseData(message="test", error=None)

    async def fake_folium_weather_map(*args, **kwargs):
        return fake_path

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.weather_map.api.weather_map_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )
    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.weather_map.api.weather_map_openwm.folium_weather_map",
        fake_folium_weather_map,
    )

    result_test_weather_map = await weather_map_service.recieve(
        api_openweathermap=settings.APPID,
        weather_layers=settings.WEATHER_LAYERS,
        logging_data=fake_logging_data,
        url_weather_map=settings.URL_WEATHER_MAPS.format(appid=settings.APPID),
        session=fake_session,
        path_to_weathermap=fake_path,
        weather_map_openwm_api=weather_map_openwm_api,
    )
    assert result_test_weather_map.error is None
    assert isinstance(result_test_weather_map.message, Path)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_weather_map_network_error(
    fake_logging_data,
    monkeypatch,
):

    fake_session = "test_session"
    fake_path = Path(__file__).resolve()

    async def fake_error_handlers(*args, **kwargs):
        return NetworkResponseData(error="network error", message=None)

    monkeypatch.setattr(
        "app.bot.modules.weather_forecast.childes.weather_map.api.weather_map_openwm.error_handler_for_the_website",
        fake_error_handlers,
    )

    result_test_weather_map = await weather_map_service.recieve(
        api_openweathermap=settings.APPID,
        weather_layers=settings.WEATHER_LAYERS,
        logging_data=fake_logging_data,
        url_weather_map=settings.URL_WEATHER_MAPS.format(appid=settings.APPID),
        session=fake_session,
        path_to_weathermap=fake_path,
        weather_map_openwm_api=weather_map_openwm_api,
    )
    assert result_test_weather_map.error == "network error"