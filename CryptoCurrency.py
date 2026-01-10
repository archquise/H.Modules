# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: CryptoCurrency
# Description: Module for displaying current cryptocurrency exchange rates.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/CryptoCurrency.png
# ---------------------------------------------------------------------------------

import logging

import aiohttp

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class CryptoCurrencyMod(loader.Module):
    """Module for displaying current cryptocurrency exchange rates."""

    strings = {
        "name": "CryptoCurrency",
        "query_missing": "Please specify a cryptocurrency ticker or name.",
        "coin_not_found": "Cryptocurrency '{query}' not found.",
    }

    strings_ru = {
        "query_missing": "Пожалуйста, укажите тикер или название криптовалюты.",
        "coin_not_found": "Криптовалюта '{query}' не найдена.",
    }

    async def fetch_json(self, url):
        """Fetch JSON data from a given URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    async def get_exchange_rates(self):
        """Get exchange rates for RUB and EUR based on USD."""
        data = await self.fetch_json("https://open.er-api.com/v6/latest/USD")
        return data["rates"]["RUB"], data["rates"]["EUR"]

    async def find_coin(self, query):
        """Find a cryptocurrency by its name or symbol."""
        data = await self.fetch_json(
            "https://api.coinlore.net/api/tickers/?start=0&limit=100"
        )
        return next(
            (
                item
                for item in data["data"]
                if query.lower() in item["name"].lower()
                or query.lower() in item["symbol"].lower()
            ),
            None,
        )

    @loader.command(
        ru_doc="Отображает текущий курс криптовалюты в рублях, долларах США и евро",
        en_doc="Displays the current cryptocurrency rate in RUB, USD, and EUR",
    )
    async def crypto(self, message):
        query = utils.get_args_raw(message)
        if not query:
            return await utils.answer(message, self.strings("query_missing"))

        coin = await self.find_coin(query)
        if not coin:
            return await utils.answer(
                message, self.strings("coin_not_found").format(query=query)
            )

        price_usd = float(coin["price_usd"])
        usd_rub_rate, usd_eur_rate = await self.get_exchange_rates()

        price_rub = price_usd * usd_rub_rate
        price_eur = price_usd * usd_eur_rate

        response = self.format_response(coin, price_usd, price_rub, price_eur)
        await utils.answer(message, response)

    def format_response(self, coin, price_usd, price_rub, price_eur):
        """Format the response message with cryptocurrency information."""
        return (
            f"💰 {coin['name']} ({coin['symbol']})\n"
            f"USD: ${price_usd:.2f}\n"
            f"RUB: ₽{price_rub:.2f}\n"
            f"EUR: €{price_eur:.2f}\n"
        )
