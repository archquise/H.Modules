# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: Article
# Description: Displays your article Criminal Code of the Russian Federation
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/Article.png
# requires: requests
# ---------------------------------------------------------------------------------

import json
import logging
import random
from typing import Dict

import requests

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ArticleMod(loader.Module):
    """Displays your article Criminal Code of the Russian Federation"""

    strings = {
        "name": "Article",
        "article": "<emoji document_id=5226512880362332956>📖</emoji> <b>Your article of the Criminal Code of the Russian Federation</b>:\n\n<blockquote>Number {}\n\n{}</blockquote>",
    }

    strings_ru = {
        "article": "<emoji document_id=5226512880362332956>📖</emoji> <b>Твоя статья УК РФ</b>:\n\n<blockquote>Номер {}\n\n{}</blockquote>",
    }

    @loader.command(
        ru_doc="Отображается ваша статья Уголовного кодекса Российской Федерации",
        en_doc="Displays your article Criminal Code of the Russian Federation",
    )
    async def arccmd(self, message):
        if values := self._load_values():
            random_key = random.choice(list(values.keys()))
            random_value = values[random_key]
            await utils.answer(
                message, self.strings("article").format(random_key, random_value)
            )

    def _load_values(self) -> Dict[str, str]:
        url = "https://raw.githubusercontent.com/Codwizer/ReModules/main/assets/zakon.json"
        try:
            response = requests.get(url)
            if response.ok:
                data = json.loads(response.text)
                return data
        except (requests.RequestException, json.JSONDecodeError):
            pass

        return {}
