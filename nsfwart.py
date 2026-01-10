# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: NSFWArt
# Description: Sends cute anime nsfw-art
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/NSFWArt.png
# ---------------------------------------------------------------------------------

import asyncio
import logging
from typing import List, Optional

import aiohttp

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class NSFWArtMod(loader.Module):
    """Sends cute anime nsfw-art"""

    strings = {
        "name": "NSFWArt",
        "fetching": "<emoji document_id=5188311512791393083>🌎</emoji> Fetching NSFW art...",
        "no_results": "<emoji document_id=5854929766146118183>❌</emoji> No results found for this tag.",
        "api_error": "<emoji document_id=5854929766146118183>❌</emoji> API error: {error}",
        "network_error": "<emoji document_id=5854929766146118183>❌</emoji> Network error. Please try again later.",
    }

    strings_ru = {
        "fetching": "<emoji document_id=5188311512791393083>🌎</emoji> Получение NSFW арта...",
        "no_results": "<emoji document_id=5854929766146118183>❌</emoji> Ничего не найдено для этого тега.",
        "api_error": "<emoji document_id=5854929766146118183>❌</emoji> Ошибка API: {error}",
        "network_error": "<emoji document_id=5854929766146118183>❌</emoji> Ошибка сети. Попробуйте позже.",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "tags",
                "drool",
                lambda: "Tag for NSFW art (e.g., drool, masturbation, yuri, etc.)",
            )
        )
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self._session

    async def _fetch_photos(self, tags: str, quantity: int = 15) -> Optional[List[str]]:
        """Fetch photos from API"""
        session = await self._get_session()

        try:
            url = f"https://api.lolicon.app/setu/v2?tag={tags}"

            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("data") and len(data["data"]) > 0:
                        return data["data"][0].get("urls", {}).get("original", [])
                    return None
                else:
                    logger.error(f"API error: {response.status}")
                    return None
        except asyncio.TimeoutError:
            logger.error("API timeout")
            return None
        except Exception as e:
            logger.error(f"Fetch error: {e}")
            return None

    async def _handle_error(self, message, error: Exception):
        """Handle different types of errors"""
        if isinstance(error, asyncio.TimeoutError):
            await utils.answer(message, self.strings("network_error"))
        else:
            await utils.answer(
                message, self.strings("api_error").format(error=str(error))
            )

    @loader.command(
        ru_doc="Отправить симпатичный NSFW-арт",
        en_doc="Send cute NSFW-art",
    )
    async def nsfwartcmd(self, message):
        """Send NSFW art based on configured tags"""
        tags = self.config["tags"]

        if not tags:
            await utils.answer(message, self.strings("no_results"))
            return

        await utils.answer(message, self.strings("fetching"))

        try:
            photos = await self._fetch_photos(tags)
            if not photos:
                await utils.answer(message, self.strings("no_results"))
                return

            await self.inline.gallery(
                message=message,
                media=photos[:15],
                caption=f"<i>{utils.ascii_face()}</i>",
            )
        except Exception as e:
            await self._handle_error(message, e)
