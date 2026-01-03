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
# Name: OneTimeMediaSaver
# Description: Save disappearing media automatically
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: OneTimeMediaSaver
# scope: OneTimeMediaSaver 0.0.1
# ---------------------------------------------------------------------------------

import logging

from telethon.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class OneTimeMediaSaverMod(loader.Module):
    """Save disappearing media automatically"""

    strings = {
        "name": "OneTimeMediaSaver",
        "saved": "✅ Media saved to Saved Messages",
        "no_reply": "🚫 Reply to disappearing media",
        "not_disappearing": "🚫 This is not disappearing media",
        "always_on": "✅ Auto-save enabled in PMs",
        "always_off": "🚫 Auto-save disabled",
        "already_on": "⚠️ Auto-save already enabled",
        "already_off": "⚠️ Auto-save already disabled",
        "status": "🔧 Auto-save status: {}",
        "on": "ON",
        "off": "OFF",
        "saved_auto": "💾 Auto-saved disappearing media",
    }

    strings_ru = {
        "saved": "✅ Медиа сохранено в Избранное",
        "no_reply": "🚫 Ответьте на исчезающее медиа",
        "not_disappearing": "🚫 Это не исчезающее медиа",
        "always_on": "✅ Автосохранение включено в ЛС",
        "always_off": "🚫 Автосохранение выключено",
        "already_on": "⚠️ Автосохранение уже включено",
        "already_off": "⚠️ Автосохранение уже выключено",
        "status": "🔧 Статус автосохранения: {}",
        "on": "ВКЛ",
        "off": "ВЫКЛ",
        "saved_auto": "💾 Автосохранено исчезающее медиа",
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self._me = await client.get_me()
        self._enabled = self._db.get(__name__, "always_enabled", False)
        self._saved_count = self._db.get(__name__, "saved_count", 0)

        client.add_event_handler(self._message_handler)

    async def on_unload(self):
        self._client.remove_event_handler(self._message_handler)

    @loader.command(
        ru_doc="[ответ] - сохранить исчезающее медиа в избранное",
        en_doc="[reply] - save disappearing media to Saved Messages",
    )
    async def s(self, message: Message):
        """Save disappearing media"""
        reply = await message.get_reply_message()

        if not reply:
            return await utils.answer(message, self.strings["no_reply"])

        if not self._is_disappearing_media(reply):
            return await utils.answer(message, self.strings["not_disappearing"])

        await self._save_media(reply)
        await utils.answer(message, self.strings["saved"])

        self._saved_count += 1
        self._db.set(__name__, "saved_count", self._saved_count)

    @loader.command(
        ru_doc="[on/off] - автосохранение исчезающего медиа в ЛС",
        en_doc="[on/off] - auto-save disappearing media in PMs",
    )
    async def salways(self, message: Message):
        """Toggle auto-save mode"""
        args = utils.get_args_raw(message).lower()

        if args == "on":
            if self._enabled:
                return await utils.answer(message, self.strings["already_on"])
            self._enabled = True
            self._db.set(__name__, "always_enabled", True)
            await utils.answer(message, self.strings["always_on"])

        elif args == "off":
            if not self._enabled:
                return await utils.answer(message, self.strings["already_off"])
            self._enabled = False
            self._db.set(__name__, "always_enabled", False)
            await utils.answer(message, self.strings["always_off"])

        elif args == "":
            status = self.strings["on"] if self._enabled else self.strings["off"]
            count = self._db.get(__name__, "saved_count", 0)
            text = f"{self.strings['status'].format(status)}\n📊 Total saved: {count}"
            await utils.answer(message, text)

        else:
            await utils.answer(message, "Use: .salways on/off")

    async def _message_handler(self, event):
        """Handle incoming messages"""
        if not self._enabled:
            return

        if not event.is_private:
            return

        if event.out:
            return

        if not self._is_disappearing_media(event):
            return

        await self._save_media(event)

        self._saved_count += 1
        self._db.set(__name__, "saved_count", self._saved_count)

    def _is_disappearing_media(self, message) -> bool:
        """Check if message contains disappearing media"""

        if not message.media:
            return False

        if hasattr(message, "ttl_period") and message.ttl_period:
            return True

        if hasattr(message, "ttl_seconds") and message.ttl_seconds:
            return True

        if message.voice and hasattr(message.voice, "ttl_seconds"):
            return True

        if message.video_note and hasattr(message.video_note, "ttl_seconds"):
            return True

        return False

    async def _save_media(self, message):
        """Save media to Saved Messages"""
        try:
            await self._client.send_message(
                "me", self.strings["saved_auto"], file=message.media, silent=True
            )
            self.logger.info(f"Saved disappearing media from user {message.sender_id}")

        except Exception as e:
            self.logger.error(f"Failed to save media: {e}")

            try:
                file = await message.download_media(file="temp/")
                await self._client.send_message(
                    "me",
                    f"{self.strings['saved_auto']}\n⚠️ Fallback method used",
                    file=file,
                    silent=True,
                )
                import os

                os.remove(file)
            except Exception as e2:
                self.logger.error(f"Fallback also failed: {e2}")
