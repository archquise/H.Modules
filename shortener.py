# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# #### Copyright (c) 2024-2029 Archquise #####

# 💬 Contact: https://t.me/archquise
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: Shortener
# Description: Module for using bit.ly API
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/Shortener.png
# ---------------------------------------------------------------------------------

import logging
import re
import aiohttp

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class Shortener(loader.Module):
    """Module for using bit.ly API"""

    strings = {
        "name": "Shortener",
        "no_api": "<emoji document_id=5854929766146118183>❌</emoji> You have not specified an API token from the site <a href='https://app.bitly.com/settings/api/'>bit.ly</a>",
        "statclcmd": "<emoji document_id=5787384838411522455>📊</emoji> <b>Statistics on clicks for this link:</b> {c}",
        "shortencmd": "<emoji document_id=5854762571659218443>✅</emoji> <b>Your shortened link is ready:</b> <code>{c}</code>",
        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> Please provide a URL to shorten.",
        "invalid_url": "<emoji document_id=5854929766146118183>❌</emoji> Invalid URL format.",
        "api_error": "<emoji document_id=5854929766146118183>❌</emoji> API error: {error}",
        "_cls_doc": "Module for using bit.ly API",
    }

    strings_ru = {
        "no_api": "<emoji document_id=5854929766146118183>❌</emoji> Вы не указали api токен с сайта <a href='https://app.bitly.com/settings/api/'>bit.ly</a>",
        "statclcmd": "<emoji document_id=5787384838411522455>📊</emoji> <b>Статистика о переходе по этой ссылке:</b> {c}",
        "shortencmd": "<emoji document_id=5854762571659218443>✅</emoji> <b>Ваша сокращённая ссылка готова:</b> <code>{c}</code>",
        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> Пожалуйста, укажите URL для сокращения.",
        "invalid_url": "<emoji document_id=5854929766146118183>❌</emoji> Неверный формат URL.",
        "api_error": "<emoji document_id=5854929766146118183>❌</emoji> Ошибка API: {error}",
        "_cls_doc": "Модуль для использования API bit.ly",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                None,
                lambda: "Need a token with https://app.bitly.com/settings/api/",
                validator=loader.validators.Hidden(),
            )
        )

    def _validate_url(self, url: str) -> bool:
        """Validate URL format"""
        if not url:
            return False

        url_pattern = re.compile(
            r"^https?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        return url_pattern.match(url) is not None

    async def shorten_url(self, url: str, token: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api-ssl.bitly.com/v4/shorten", json={'long_url': url}, headers={"Authorization": f"Bearer {token}"}) as resp:
                if resp.status == 201:
                    json_response = await resp.json()
                    return json_response['link']
                else:
                    logger.error(f"Error occurred! Status code: {resp.status}")
                    return
    
    async def get_bitlink_stats(self, bitlink: str, token: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary", headers={"Authorization": f"Bearer {token}"}) as resp:
                if resp.status == 200:
                    json_response = await resp.json()
                    return json_response['total_clicks']
                else:
                    logger.error(f"Error occurred! Status code: {resp.status}")
                    return



    @loader.command(
        ru_doc="Сократить ссылку через bit.ly (ссылка с https://)",
        en_doc="Shorten the link via bit.ly (url with https://)",
    )
    async def shortencmd(self, message):
        """Shorten URL using bit.ly API"""
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_api"))
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return

        if not self._validate_url(args):
            await utils.answer(message, self.strings("invalid_url"))
            return

        try:
            short_url = await self.shorten_url(url=args, token=self.config['token'])
            await utils.answer(message, self.strings("shortencmd").format(c=short_url))
        except Exception as e:
            logger.error(f"Error shortening URL: {e}")
            await utils.answer(message, self.strings("api_error").format(error=str(e)))

    @loader.command(
        ru_doc="Посмотреть статистику ссылки через bit.ly (ссылка без https:// | Доступно только на платных аккаунтах)",
        en_doc="View link statistics via bit.ly (link without https:// | Works only on paid accounts)",
    )
    async def statclcmd(self, message):
        """Get click statistics for shortened URL"""
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_api"))
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return

        try:
            if not args.startswith("bit.ly/"):
                await utils.answer(message, self.strings("invalid_url"))
                return
            else:
                clicks = await self.get_bitlink_stats(bitlink=args, token=self.config['token'])
                await utils.answer(message, self.strings("statclcmd").format(c=clicks))
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            await utils.answer(message, self.strings("api_error").format(error=str(e)))
