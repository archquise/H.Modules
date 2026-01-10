# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: animals
# Description: Random cats and dogs
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/animals.png
# requires: requests
# ---------------------------------------------------------------------------------

import logging

import requests

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class animals(loader.Module):
    """Random cats and dogs"""

    strings = {
        "name": "animals",
        "loading": "<b>Generation is underway</b> <emoji document_id=5215484787325676090>🕐</emoji>",
        "done": "<b>Here is your salute</b> <emoji document_id=5436246187944460315>❤️</emoji>",
    }

    strings_ru = {
        "loading": "<b>Генерация идет полным ходом</b> <emoji document_id=5215484787325676090>🕐</emoji>",
        "done": "<b>Вот ваш результат</b> <emoji document_id=5436246187944460315>❤️</emoji>",
    }

    # thanks https://github.com/C0dwiz/H.Modules/pull/1
    async def get_photo(self, prefix: str) -> str:
        response = requests.get(f"https://api.{prefix}.com/v1/images/search")
        return response.json()[0]["url"]

    @loader.command(
        ru_doc="Файлы случайных фотографий кошек",
        en_doc="Random photos of cats files",
    )
    async def fcatcmd(self, message):
        await utils.answer(message, self.strings("loading"))
        cat_url = await self.get_photo("thecatapi")
        await utils.answer_file(
            message, cat_url, self.strings("done"), force_document=True
        )

    @loader.command(
        ru_doc="Случайные фотографии собачьих файлов",
        en_doc="Random photos of dog files",
    )
    async def fdogcmd(self, message):
        await utils.answer(message, self.strings("loading"))
        dog_url = await self.get_photo("thedogapi")
        await utils.answer_file(
            message, dog_url, self.strings("done"), force_document=True
        )

    @loader.command(
        ru_doc="Случайные фотографии кошек",
        en_doc="Random photos of cats",
    )
    async def catcmd(self, message):
        await utils.answer(message, self.strings("loading"))
        cat_url = await self.get_photo("thecatapi")
        await utils.answer_file(
            message, cat_url, self.strings("done"), force_document=False
        )

    @loader.command(
        ru_doc="Случайные фотографии собаки",
        en_doc="Random photos of dog",
    )
    async def dogcmd(self, message):
        await utils.answer(message, self.strings("loading"))
        dog_url = await self.get_photo("thedogapi")
        await utils.answer_file(
            message, dog_url, self.strings("done"), force_document=False
        )
