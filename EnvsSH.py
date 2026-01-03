# Proprietary License Agreement

# Copyright (c) 2024-29 CodWiz

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

# 4. Any use of the Software must include the above copyright notice and this permission notice in all copies or substantial portions of the Software.

# 5. By using the Software, you agree to be bound by the terms and conditions of this license.

# For any inquiries or requests for permissions, please contact codwiz@yandex.ru.

# ---------------------------------------------------------------------------------
# Name: EnvsSH
# Description: Module for reuploading files to envs.sh
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api EnvsSH
# scope: Api EnvsSH 0.0.1
# requires: aiohttp
# ---------------------------------------------------------------------------------

import logging
import os

import aiohttp

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class EnvsSHMod(loader.Module):
    """Upload files to envs.sh"""

    strings = {
        "name": "EnvsSH",
        "no_reply": "❌ Reply to a file",
        "uploading": "📤 Uploading {}...",
        "success": "✅ Uploaded\n\n🔗 {}",
        "error": "❌ Upload failed",
        "size_error": "❌ File too large",
        "connection_error": "❌ Connection failed",
    }

    strings_ru = {
        "no_reply": "❌ Ответьте на файл",
        "uploading": "📤 Загружаю {}...",
        "success": "✅ Загружено\n\n🔗 {}",
        "error": "❌ Ошибка загрузки",
        "size_error": "❌ Файл слишком большой",
        "connection_error": "❌ Ошибка соединения",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "max_size_mb",
                100,
                "Maximum file size in MB",
                validator=loader.validators.Integer(minimum=1, maximum=500),
            ),
            loader.ConfigValue(
                "auto_delete",
                True,
                "Auto delete file after upload",
                validator=loader.validators.Boolean(),
            ),
        )
        self.session = None

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))

    async def on_unload(self):
        if self.session:
            await self.session.close()

    @loader.command(
        ru_doc="[ответ] - загрузить файл на envs.sh",
        en_doc="[reply] - upload file to envs.sh",
    )
    async def envs(self, message):
        """Upload file to envs.sh"""
        reply = await message.get_reply_message()
        if not reply or not reply.document:
            return await utils.answer(message, self.strings["no_reply"])

        filename = reply.file.name or "file.bin"
        msg = await utils.answer(message, self.strings["uploading"].format(filename))

        try:
            file_path = await reply.download_media(file="temp/")

            file_size = os.path.getsize(file_path)
            max_size = self.config["max_size_mb"] * 1024 * 1024

            if file_size > max_size:
                os.remove(file_path)
                return await msg.edit(self.strings["size_error"])

            url = await self._upload_to_envs(file_path)

            await msg.edit(self.strings["success"].format(url))

            if self.config["auto_delete"]:
                os.remove(file_path)

        except aiohttp.ClientConnectionError:
            await msg.edit(self.strings["connection_error"])
        except Exception:
            await msg.edit(self.strings["error"])
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:  # noqa: E722
                pass

    async def _upload_to_envs(self, file_path: str) -> str:
        """Upload file to envs.sh and return URL"""
        with open(file_path, "rb") as f:
            form = aiohttp.FormData()
            form.add_field("files[]", f, filename=os.path.basename(file_path))

            async with self.session.post("https://envs.sh", data=form) as response:
                response.raise_for_status()
                data = await response.json()
                return data["files"][0]["url"]
