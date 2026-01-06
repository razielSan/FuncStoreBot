# Responses, strings, text for module proxies.childes.webshare
from pathlib import Path

from app.app_utils.module_loader.loader import get_child_modules_settings_inline_data
from app.app_utils.keyboards import get_total_buttons_inline_kb
from app.bot.core.paths import bot_path


inline_data = get_child_modules_settings_inline_data(
    module_path=bot_path.BOT_DIR / "modules" / Path("proxies/childes/webshare/childes"),
    root_package="app.bot.modules.proxies.childes.webshare.childes",
)

get_keyboards_menu_buttons = get_total_buttons_inline_kb(
    list_inline_kb_data=inline_data, quantity_button=1
)
