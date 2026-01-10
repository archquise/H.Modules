# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: InlineCoin
# Description: Mini game heads or tails.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/InlineCoin.png
# ---------------------------------------------------------------------------------

import logging
import random
from typing import Dict

from .. import loader
from ..inline.types import InlineQuery

logger = logging.getLogger(__name__)


@loader.tds
class CoinFlipMod(loader.Module):
    """Mini coin flip game"""

    strings = {
        "name": "InlineCoin",
        "titles": "🪙 Heads or Tails?",
        "description": "🎲 Let's find out!",
        "heads": "🦅 An eagle fell out!",
        "tails": "🪙 Tails fell out!",
        "edge": "🙀 Miraculously, the coin remained on its edge!",
        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> Please provide a command to flip.",
        "error_general": "<emoji document_id=5854929766146118183>❌</emoji> An error occurred: {error}",
    }

    strings_ru = {
        "titles": "🪙 Орёл или решка?",
        "description": "🎲 Давай узнаем!",
        "heads": "🦅 Выпал орёл!",
        "tails": "🪙 Выпала решка!",
        "edge": "🙀 Чудо, монетка осталась на ребре!",
        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> Укажите команду для подбрасывания монетки.",
        "error_general": "<emoji document_id=5854929766146118183>❌</emoji> Произошла ошибка: {error}",
    }

    def get_coin_flip_result(self) -> Dict[str, str]:
        """Get coin flip result with better formatting"""
        return {
            "title": self.strings["titles"],
            "description": self.strings["description"],
            "message": f"<b>{random.choice([self.strings['heads'], self.strings['tails']])}</b>",
            "thumb": "https://github.com/Codwizer/ReModules/blob/main/assets/images.png",
        }

    @loader.command(
        ru_doc="Подбросить монетку",
        en_doc="Flip a coin",
    )
    async def coin_inline_handler(self, query: InlineQuery):
        """Handle coin flip inline query"""
        if not query.args:
            return {
                "title": self.strings["titles"],
                "description": self.strings["no_args"],
                "message": self.strings["no_args"],
            }

        result = self.get_coin_flip_result()
        return {
            "title": self.strings["titles"],
            "description": self.strings["description"],
            "message": result["message"],
            "thumb": result["thumb"],
        }
