# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# #### Copyright (c) 2024-2029 Archquise #####

# 💬 Contact: https://t.me/archquise
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: CodeShare
# Description: Uploads your code at the kmi.aeza.net (Pastebin and GitHub Gist alternative)
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/CodeShare.png
# requires: aiofiles
# ---------------------------------------------------------------------------------

import aiohttp
import aiofiles
import logging

from .. import loader, utils
from telethon.types import MessageMediaDocument

logger = logging.getLogger(__name__)


@loader.tds
class CodeShareMod(loader.Module):
    """Uploads your code at the kmi.aeza.net (Pastebin and GitHub Gist alternative)"""

    strings = {
        "name": "CodeShare",
        "invalid_args": "<emoji document_id=5854929766146118183>❌</emoji> There is no arguments or reply with a file, or they are invalid",
        "_cls_doc": "Uploads your code at the kmi.aeza.net (Pastebin and GitHub Gist alternative)",
        "link_ready": "<emoji document_id=5854762571659218443>✅</emoji> <b>Code uploaded! Link:</b> <code>{}</code>",
    }

    strings_ru = {
        "_cls_doc": "Загружает ваш код на kmi.aeza.net (альтернатива Pastebin и GitHub Gist)",
        "invalid_args": "<emoji document_id=5854929766146118183>❌</emoji> Нет аргументов или реплая с файлом, или они неверны",
        "link_ready": "<emoji document_id=5854762571659218443>✅</emoji> <b>Код загружен! Ссылка:</b> <code>{}</code>",
    }

    async def upload_to_kmi(self, content: str) -> str:
        url = "https://kmi.aeza.net"
        data = aiohttp.FormData()
        data.add_field("kmi", content)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    link = await response.text()
                    return link
                else:
                    logger.error(f"Error occurred! Status code: {response.status}")
                    return

    @loader.command(
        ru_doc="Загрузка кода на сайт",
        en_doc="Upload code to the site",
    )
    async def codesharecmd(self, message):
        args = utils.get_args(message)
        reply = await message.get_reply_message()
        if args:
            link = await self.upload_to_kmi(args)
            await utils.answer(message, self.strings["link_ready"].format(link))
            return
        if reply and isinstance(reply.media, MessageMediaDocument):
            file_name = await reply.download_media()
            async with aiofiles.open(file_name, mode="r") as f:
                content = await f.read()
            link = await self.upload_to_kmi(content)
            await aiofiles.os.remove(file_name)
            await utils.answer(message, self.strings["link_ready"].format(link))
            return
        await utils.answer(message, self.strings["invalid_args"])
