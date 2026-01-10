# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# #### Copyright (c) 2024-2029 Archquise #####

# 💬 Contact: https://t.me/archquise
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: WindowsKeys
# Description: Provides you Windows activation keys
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/WindowsKeys.png
# requires: requests
# ---------------------------------------------------------------------------------

import logging
import time

import aiohttp

from .. import loader

logger = logging.getLogger(__name__)


@loader.tds
class WindowsKeysMod(loader.Module):
    """Windows activation keys"""

    strings = {
        "name": "WindowsKeys",
        "winkey": "✅ Key: <code>{}</code>\n\n⚠ For KMS activation only",
        "error": "❌ Failed to get key",
        "select": "🔓 Select version:",
        "close": "🎈 Close",
        "loading": "⌛ Loading...",
    }

    strings_ru = {
        "winkey": "✅ Ключ: <code>{}</code>\n\n⚠ Только для KMS активации",
        "error": "❌ Ошибка получения",
        "select": "🔓 Выберите версию:",
        "close": "🎈 Закрыть",
        "loading": "⌛ Загрузка...",
    }

    def __init__(self):
        self.cache = None
        self.cache_time = 0
        self.CACHE_TTL = 3600

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command(ru_doc="Меню ключей Windows", en_doc="Windows keys menu")
    async def winkey(self, message):
        await self.inline.form(
            self.strings["select"],
            message=message,
            reply_markup=[
                [
                    {
                        "text": "Win 10/11 Pro",
                        "callback": self._key,
                        "args": ("win10_11pro",),
                    }
                ],
                [
                    {
                        "text": "Win 10/11 LTSC",
                        "callback": self._key,
                        "args": ("win10_11enterpriseLTSC",),
                    }
                ],
                [
                    {
                        "text": "Win 8.1 Pro",
                        "callback": self._key,
                        "args": ("win8.1pro",),
                    }
                ],
                [{"text": "Win 8 Pro", "callback": self._key, "args": ("win8pro",)}],
                [{"text": "Win 7 Pro", "callback": self._key, "args": ("win7pro",)}],
                [
                    {
                        "text": "Vista Business",
                        "callback": self._key,
                        "args": ("winvistabusiness",),
                    }
                ],
                [{"text": self.strings["close"], "action": "close"}],
            ],
        )

    async def _key(self, call, version):
        await call.edit(self.strings["loading"])
        keys = await self._get_keys()
        key = keys.get(version) if keys else None
        await call.edit(
            self.strings["winkey"].format(key) if key else self.strings["error"],
            reply_markup=[
                [{"text": "← Back", "callback": self.winkey}],
                [{"text": self.strings["close"], "action": "close"}],
            ],
        )

    async def _get_keys(self):
        if time.time() - self.cache_time < self.CACHE_TTL:
            return self.cache

        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(10)
            ) as session:
                async with session.get("https://files.archquise.ru/winkeys.json") as r:
                    self.cache = await r.json()
                    self.cache_time = time.time()
                    return self.cache
        except Exception:  # noqa: E722
            return None
