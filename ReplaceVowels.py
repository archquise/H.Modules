# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: VowelReplacer
# Description: Replaces vowel letters with ё
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/VowelReplacer.png
# ---------------------------------------------------------------------------------

import logging

from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class VowelReplacer(loader.Module):
    """Replaces vowel letters with ё"""

    strings = {
        "name": "Vowel Replacer",
        "on": "✅ Vowel substitution for ё has been successfully enabled.",
        "off": "🚫 Vowel substitution for ё is disabled.",
    }

    strings_ru = {
        "on": "✅ Замена гласных на ё успешно включена.",
        "off": "🚫 Замена гласных на ё отключена.",
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.enabled = self.db.get("vowel_replacer", "enabled", False)

    @loader.command(
        ru_doc="Включить или отключить замену гласных на ё.",
        en_doc="Enable or disable vowel substitution for ё.",
    )
    async def vowelreplace(self, message):
        self.enabled = not self.enabled
        self.db.set("vowel_replacer", "enabled", self.enabled)

        if self.enabled:
            response = self.strings("on")
        else:
            response = self.strings("off")

        await utils.answer(message, response)

    async def watcher(self, message: Message):
        """Автоматическая замена гласных на ё при получении собственного сообщения."""
        if self.enabled and message.out:
            vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
            message_text = message.text
            replaced_text = "".join(
                "ё" if char in vowels else char for char in message_text
            )

            await message.edit(replaced_text)
