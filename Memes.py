# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: Meme
# Description: Random memes
# Author: @hikka_mods
# Commands:
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/InlineMemes.png
# ---------------------------------------------------------------------------------

import logging
import random  # noqa: F401

import aiohttp  # noqa: F401
from bs4 import BeautifulSoup  # noqa: F401

from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class MemesMod(loader.Module):
    """Random memes"""

    strings = {
        "name": "Memes",
        "done": "☄️ Catch the meme",
        "still": "🔄 Update",
        "dell": "❌ Close",
    }

    strings_ru = {
        "done": "☄️ Лови мем",
        "still": "🔄 Обновить",
        "dell": "❌ Закрыть",
    }

    async def client_ready(self, client, db):
        self.hmodslib = await self.import_lib(
            "https://files.archquise.ru/HModsLibrary.py"
        )

    @loader.command(
        ru_doc="",
        en_doc="",
    )
    async def memescmd(self, message):
        img = await self.hmodslib.get_random_image()
        await self.inline.form(
            text=self.strings("done"),
            photo=img,
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("still"),
                        "callback": self.ladno,
                    }
                ],
                [
                    {
                        "text": self.strings("dell"),
                        "callback": self.dell,
                    }
                ],
            ],
            silent=True,
        )

    async def ladno(self, call):
        img = await self.hmodslib.get_random_image()
        await call.edit(
            text=self.strings("done"),
            photo=img,
            reply_markup=[
                [
                    {
                        "text": self.strings("still"),
                        "callback": self.ladno,
                    }
                ],
                [
                    {
                        "text": self.strings("dell"),
                        "callback": self.dell,
                    }
                ],
            ],
        )

    async def dell(self, call):
        """Callback button"""
        await call.delete()
