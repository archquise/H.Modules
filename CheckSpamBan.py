# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: CheckSpamBan
# Description: Check spam ban for your account.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/CheckSpamBan.png
# ---------------------------------------------------------------------------------

import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class SpamBanCheckMod(loader.Module):
    """Checks spam ban for your account."""

    strings = {
        "name": "CheckSpamBan",
    }

    @loader.command(
        ru_doc="Проверяет вашу учетную запись на спам-бан с помощью бота @SpamBot",
        en_doc="Checks your account for spam ban via @SpamBot bot",
    )
    async def spambot(self, message):
        async with self.client.conversation(178220800) as conv:
            user_message = await conv.send_message("/start")
            await user_message.delete()
            spam_message = await conv.get_response()
        await utils.answer(message, spam_message.text)
        await spam_message.delete()
