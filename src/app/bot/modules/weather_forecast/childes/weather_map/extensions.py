from typing import Dict, Tuple
from pathlib import Path

import folium


async def folium_weather_map(
    location: Tuple,
    zoom: int,
    weather_layers: Dict,
    path: Path,
    overlay: bool,
    control: bool,
    opacity: float,
    api_openweathermap: str,
) -> Path:
    m = folium.Map(location=location, zoom_start=zoom)

    # Добавляем каждый слой
    for name, layer in weather_layers.items():
        folium.TileLayer(
            tiles=f"https://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={api_openweathermap}",
            attr="OpenWeatherMap",
            name=name,
            overlay=overlay,  # чтобы слой был поверх базовой карты
            control=control,  # чтобы можно было включать/выключать
            opacity=opacity,  # прозрачность (0 — прозрачный, 1 — непрозрачный)
        ).add_to(m)

    folium.LayerControl().add_to(m)  # Добавляем управление слоями
    m.save(path)  # cохраняем карту погоды
    return path
