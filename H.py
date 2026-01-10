# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: H
# Description: H.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/H.png
# ---------------------------------------------------------------------------------

from .. import loader, utils


@loader.tds
class H(loader.Module):
    """H"""

    strings = {"name": "H", "h": "H"}
    strings_ru = {"h": "H"}

    @loader.command(
        ru_doc="H",
    )
    async def h(self, message):
        """H"""
        await utils.answer(message, self.strings("h"))
