# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: AnimeQuotes
# Description: A module for sending random quotes from anime
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/AnimeQuotes.png
# requires: requests
# ---------------------------------------------------------------------------------

import logging

import aiohttp

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class AnimeQuotesMod(loader.Module):
    """A module for sending random quotes from anime"""

    strings = {
        "name": "AnimeQuotes",
        "quote_template": (
            '<b>Quote:</b> "{quote}"\n\n'
            "<b>Character:</b> {character}\n"
            "<b>Anime:</b> {anime}"
        ),
        "error": "<b>Couldn't get a quote. Try again later!</b>",
    }

    strings_ru = {
        "quote_template": (
            '<b>Цитата:</b> "{quote}"\n\n'
            "<b>Персонаж:</b> {character}\n"
            "<b>Аниме:</b> {anime}"
        ),
        "error": "<b>Не удалось получить цитату. Попробуйте позже!</b>",
    }

    @loader.command(
        ru_doc="Получить случайную цитату из аниме",
        en_doc="Get a random quote from the anime",
    )
    async def quote(self, message):
        url = "https://api.animechan.io/v1/quotes/random"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()

                    quote_content = data["data"]["content"]
                    character_name = data["data"]["character"]["name"]
                    anime_name = data["data"]["anime"]["name"]

                    quote = self.strings["quote_template"].format(
                        quote=quote_content, character=character_name, anime=anime_name
                    )
                    await utils.answer(message, quote)

        except aiohttp.ClientError:
            await utils.answer(message, self.strings["error"])
