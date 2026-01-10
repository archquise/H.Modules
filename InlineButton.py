# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: InlineButton
# Description: Create inline button
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/InlineButton.png
# ---------------------------------------------------------------------------------

import logging

from .. import loader, utils
from ..inline.types import InlineQuery

logger = logging.getLogger(__name__)


@loader.tds
class InlineButtonMod(loader.Module):
    """Create inline buttons with enhanced functionality"""

    strings = {
        "name": "InlineButton",
        "titles": "🔘 Create message with Inline Button",
        "error_title": "<emoji document_id=5854929766146118183>❌</emoji> Error",
        "error_description": "<emoji document_id=5854929766146118183>❌</emoji> Invalid input format. Please provide exactly three comma-separated values: message, name, url.",
        "error_message": "<emoji document_id=5854929766146118183>❌</emoji> Make sure your input is formatted as: message, name, url.",
        "button_created": "<emoji document_id=5854762571659218443>✅</emoji> Button created successfully!",
        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> Please provide arguments: message, name, url.",
    }

    strings_ru = {
        "titles": "🔘 Создать сообщение с Inline Кнопкой",
        "error_title": "<emoji document_id=5854929766146118183>❌</emoji> Ошибка",
        "error_description": "<emoji document_id=5854929766146118183>❌</emoji> Неверный формат ввода. Пожалуйста, укажите ровно три значения, разделенных запятыми: сообщение, имя, url.",
        "error_message": "<emoji document_id=5854929766146118183>❌</emoji> Убедитесь, что ваш ввод имеет следующий формат: сообщение, имя, url.",
        "button_created": "<emoji document_id=5854762571659218443>✅</emoji> Кнопка успешно создана!",
        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> Укажите аргументы: сообщение, имя, url.",
    }

    @loader.command(
        ru_doc="Создать inline кнопку\nНапример: @username_bot crinl Текст сообщения, Текст кнопки, Ссылка в кнопке",
        en_doc="Create an inline button\nexample: @username_bot crinl Message text, Button text, Link in the button",
    )
    async def crinl_inline_handler(self, query: InlineQuery):
        args = utils.get_args_raw(query.query)

        if not args:
            return {
                "title": self.strings("error_title"),
                "description": self.strings("error_description"),
                "message": self.strings("no_args"),
            }

        args_list = [arg.strip() for arg in args.split(",")]

        if len(args_list) != 3:
            return {
                "title": self.strings("error_title"),
                "description": self.strings("error_description"),
                "message": self.strings("error_message"),
            }

        message, name, url = args_list
        return True, {
            "message": message,
            "reply_markup": [{"text": name, "url": url}],
            "description": self.strings("button_created"),
        }
