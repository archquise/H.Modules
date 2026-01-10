# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: Text2File
# Description: Module for convertation your text to file
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/Text2File.png
# ---------------------------------------------------------------------------------

import io
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class Text2File(loader.Module):
    """Module for convertation your text to file"""

    strings = {
        "name": "Text2File",
        "no_args": "Don't have any args! Use .ttf text/code",
        "cfg_name": "You can change the extension and file name",
    }

    strings_ru = {
        "no_args": "Недостаточно аргументов! Используйте: .ttf текст/код",
        "cfg_name": "Вы можете выбрать расширение и название для файла",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "name",
                "file.txt",
                lambda: self.strings("cfg_name"),
            ),
        )

    @loader.command(
        ru_doc="Создать файл с вашим текстом или кодом",
        en_doc="Create a file with your text or code",
    )
    async def ttfcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return

        text = args
        by = io.BytesIO(text.encode("utf-8"))
        by.name = self.config["name"]

        await utils.send_file(
            message.chat_id,
            by,
            caption=None,
            reply_to=message.reply_to_msg_id,
        )
