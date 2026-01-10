# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: SMArchiver
# Description: unloads all messages from Favorites
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/SMArchiver.png
# requires: zipfile
# ---------------------------------------------------------------------------------

import logging
import os
import zipfile
from datetime import datetime

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class SMArchiver(loader.Module):
    """unloads all messages from Favorites"""

    strings = {
        "name": "SMArchiver",
        "archive_created": "🎉 Archive with messages has been successfully created: {filename}",
        "no_messages": "⚠️ There are no messages in Saved Messages.",
        "error": "❌ An error occurred: {error}",
        "processing": "🛠️ Processing messages... Please wait.\n\nP.S: Be careful, if you have a lot of messages, you may get flooding, and if you have a lot of heavy files, the download will be slower than usual.",
    }

    strings_ru = {
        "archive_created": "🎉 Архив с сообщениями успешно создан: {filename}",
        "no_messages": "⚠️ В Сохраненных сообщениях нет сообщений.",
        "error": "❌ Произошла ошибка: {error}",
        "processing": "🛠️ Обработка сообщений... Пожалуйста, подождите.\n\nP.S: Будьте осторожны, если у вас много сообщений, вы можете получить флуд, а если у вас много тяжелых файлов, загрузка будет медленнее обычного.",
    }

    @loader.command(
        ru_doc="выгружает все сообщения из Избранного / Saved Messages и собирает их в одном архиве.",
        en_doc="downloads all messages from Favorites / Saved Messages and collects them in one archive.",
    )
    async def smdump(self, message):
        await utils.answer(message, self.strings["processing"])
        saved_messages = await message.client.get_messages("me", limit=None)

        if not saved_messages:
            await utils.answer(message, self.strings["no_messages"])
            return

        archive_path = await self.create_archive(saved_messages)

        try:
            await message.client.send_file(
                message.chat_id,
                archive_path,
                caption=self.strings["archive_created"].format(
                    filename=os.path.basename(archive_path)
                ),
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(error=str(e)))
        finally:
            self.cleanup(archive_path)

    async def create_archive(self, saved_messages):
        current_month = datetime.now().strftime("%B %Y")
        archive_path = "saved_messages.zip"

        with zipfile.ZipFile(archive_path, "w") as archive:
            self.initialize_archive_structure(archive, current_month)
            for msg in saved_messages:
                await self.add_message_to_archive(msg, archive, current_month)

        return archive_path

    def initialize_archive_structure(self, archive, current_month):
        month_folder = f"{current_month}/"
        archive.writestr(month_folder, "")
        message_folders = {
            "Text Messages": f"{month_folder}Text Messages/",
            "Voice Messages": f"{month_folder}Voice Messages/",
            "Video Messages": f"{month_folder}Video Messages/",
            "Videos": f"{month_folder}Videos/",
            "Audios": f"{month_folder}Audios/",
            "GIFs": f"{month_folder}GIFs/",
            "Files": f"{month_folder}Files/",
        }

        for folder in message_folders.values():
            archive.writestr(folder, "")

    async def add_message_to_archive(self, msg, archive, current_month):
        """Обрабатывает отдельное сообщение и добавляет его в архив."""
        if msg.message:
            await self.add_text_message_to_archive(msg, archive, current_month)

        if msg.media:
            await self.add_media_to_archive(msg, archive, current_month)

    async def add_text_message_to_archive(self, msg, archive, current_month):
        timestamp = datetime.fromtimestamp(msg.date.timestamp()).strftime(
            "%Y%m%d_%H%M%S"
        )
        safe_name = f"message_{timestamp}.txt"
        archive.writestr(
            os.path.join(f"{current_month}/Text Messages/", safe_name), msg.message
        )

    async def add_media_to_archive(self, msg, archive, current_month):
        media_file = await msg.client.download_media(msg.media)
        if media_file:
            mime_type = (
                msg.media.document.mime_type if hasattr(msg.media, "document") else None
            )
            folder = self.get_media_folder(mime_type, current_month)
            archive.write(
                media_file, os.path.join(folder, os.path.basename(media_file))
            )

    def get_media_folder(self, mime_type, current_month):
        if mime_type:
            if mime_type.startswith("audio/"):
                return f"{current_month}/Audios/"
            elif mime_type.startswith("video/"):
                return f"{current_month}/Videos/"
            elif mime_type.startswith("image/gif"):
                return f"{current_month}/GIFs/"
        return f"{current_month}/Files/"

    def cleanup(self, archive_path):
        if os.path.exists(archive_path):
            os.remove(archive_path)
