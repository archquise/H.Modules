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
# Name: MessageMonitor
# Description: Monitor messages for trigger words in all chats.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: MessageMonitor
# scope: MessageMonitor 0.0.1
# ---------------------------------------------------------------------------------

import logging
import re

from herokutl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class MessageMonitor(loader.Module):
    """
    Monitor messages for trigger words in all chats.
    """

    strings = {
        "name": "MessageMonitor",
        "triggers_set": "Trigger words have been set: {}",
        "triggers_not_set": "Trigger words have not been set",
        "target_set": "Target chat for notifications has been set",
        "target_not_set": "Target chat for notifications has not been set",
        "monitoring_started": "Monitoring has started",
        "monitoring_stopped": "Monitoring has stopped",
        "monitoring_status": "Monitoring {}",
        "triggers_example": "Example: <code>.triggers word1 word2</code>",
        "monitoring_status_on": "enabled",
        "monitoring_status_off": "disabled",
        "ignore_set": "Ignored chats have been set: {}",
        "ignore_none": "Ignored chats have not been set",
        "ignore_example": "Example: <code>.ignore 123456789 -987654321</code> (chat IDs)",
        "no_reply": "Reply to a message in the desired chat or specify its ID",
        "monitoring_msg": (
            "🚨 **Trigger word detected!** 🚨\n\n"
            "**Chat:** {} (`{}`)\n"
            "**User:** {}\n"
            "**Link:** {}\n\n"
            "**Messages:**\n{}"
        ),
    }

    strings_ru = {
        "triggers_set": "Триггерные слова установлены: {}",
        "triggers_not_set": "Триггерные слова не установлены",
        "target_set": "Целевой чат для уведомлений установлен",
        "target_not_set": "Целевой чат для уведомлений не установлен",
        "monitoring_started": "Мониторинг запущен",
        "monitoring_stopped": "Мониторинг остановлен",
        "monitoring_status": "Мониторинг {}",
        "triggers_example": "Пример: <code>.triggers слово1 слово2</code>",
        "monitoring_status_on": "включен",
        "monitoring_status_off": "выключен",
        "ignore_set": "Игнорируемые чаты установлены: {}",
        "ignore_none": "Игнорируемые чаты не установлены",
        "ignore_example": "Пример: <code>.ignore 123456789 -987654321</code> (ID чатов)",
        "no_reply": "Ответьте на сообщение в нужном чате или укажите его ID",
        "monitoring_msg": (
            "🚨 **Обнаружено триггерное слово!** 🚨\n\n"
            "**Чат:** {} (`{}`)\n"
            "**Пользователь:** {}\n"
            "**Ссылка:** {}\n\n"
            "**Сообщение:**\n{}"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "triggers",
                [],
                "Список триггерных слов",
                validator=loader.validators.Series(),
            ),
            loader.ConfigValue(
                "target_chat",
                None,
                "ID целевого чата для отправки уведомлений",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "ignore_chats",
                [],
                "Список ID чатов, которые будут игнорироваться",
                validator=loader.validators.Series(),
            ),
        )
        self._triggers = []
        self._target_chat = None
        self._ignore_chats = []

    async def client_ready(self, client, db):
        self._triggers = self.config["triggers"]
        self._target_chat = self.config["target_chat"]
        self._ignore_chats = [
            int(i)
            for i in self.config["ignore_chats"]
            if str(i).isdigit() or str(i).startswith("-")
        ]
        self.client = client

    @loader.command(
        ru_doc="Установить триггерные слова. Пример: .triggers слово1 слово2",
        en_doc="Set trigger words. Example: .triggers word1 word2",
    )
    async def triggers(self, message: Message):
        """Set trigger words"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings["triggers_example"])
            return

        self._triggers = [arg.lower() for arg in args]
        self.config["triggers"] = self._triggers
        await utils.answer(
            message, self.strings["triggers_set"].format(", ".join(self._triggers))
        )

    @loader.command(
        ru_doc="Установить целевой чат для уведомлений. Ответьте на сообщение или укажите ID",
        en_doc="Set target chat for notifications. Reply to a message or provide its ID",
    )
    async def settarget(self, message: Message):
        """Set target chat"""
        args = utils.get_args_raw(message)
        chat_id = None

        if getattr(message, "is_reply", False):
            get_reply_method = getattr(message, "get_reply_message", None)
            if get_reply_method:
                reply_message = await get_reply_method()
                if reply_message and getattr(reply_message, "chat_id", None):
                    chat_id = reply_message.chat_id
        elif args and (args.isdigit() or args.startswith("-") and args[1:].isdigit()):
            chat_id = int(args)

        if chat_id:
            self.config["target_chat"] = chat_id
            self._target_chat = chat_id
            await utils.answer(message, self.strings["target_set"])
        else:
            await utils.answer(message, self.strings["no_reply"])

    @loader.command(
        ru_doc="Установить игнорируемые чаты. Укажите ID чатов через пробел.",
        en_doc="Set ignored chats. Provide chat IDs separated by space.",
    )
    async def ignore(self, message: Message):
        """Set ignored chats"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings["ignore_example"])
            return

        valid_ids = []
        for arg in args:
            if arg.isdigit() or (arg.startswith("-") and arg[1:].isdigit()):
                valid_ids.append(int(arg))

        self.config["ignore_chats"] = valid_ids
        self._ignore_chats = valid_ids

        if valid_ids:
            await utils.answer(
                message,
                self.strings["ignore_set"].format(", ".join(map(str, valid_ids))),
            )
        else:
            await utils.answer(
                message, "Не удалось распознать ID чатов. Используйте только числа."
            )

    @loader.watcher(out=False, only_messages=True)
    async def message_watcher(self, message: Message):
        """Watch for messages containing trigger words"""

        if not self._target_chat or not self._triggers:
            return

        chat_id = getattr(message, "chat_id", None)

        if chat_id and chat_id in self._ignore_chats:
            logger.debug(f"Message in ignored chat: {chat_id}. Skipping monitoring.")
            return

        text = getattr(message, "text", "")
        if not text:
            return

        text_lower = text.lower()

        found_triggers = [
            trigger
            for trigger in self._triggers
            if re.search(r"\b" + re.escape(trigger) + r"\b", text_lower)
        ]

        if not found_triggers:
            return

        try:
            get_chat_method = getattr(message, "get_chat", None)
            if get_chat_method:
                chat = await get_chat_method()
                chat_title = getattr(
                    chat,
                    "title",
                    "Личные сообщения"
                    if getattr(message, "is_private", False)
                    else "Чат с ID " + str(chat_id),
                )
            else:
                chat_title = "Неизвестный чат"

            get_sender_method = getattr(message, "get_sender", None)
            if get_sender_method:
                sender = await get_sender_method()
                sender_name = sender.first_name
                if getattr(sender, "last_name", None):
                    sender_name += f" {sender.last_name}"
                if not sender_name:
                    sender_name = getattr(
                        sender, "username", "Неизвестный пользователь"
                    )
            else:
                sender_name = "Неизвестный пользователь"

            to_id_obj = getattr(message, "to_id", None)
            if to_id_obj and getattr(to_id_obj, "channel_id", None):
                link = f"https://t.me/c/{to_id_obj.channel_id}/{message.id}"
            elif getattr(message, "is_private", False) and getattr(
                sender, "username", None
            ):
                link = f"https://t.me/{sender.username}/{message.id}"

            await self.client.send_message(
                self._target_chat,
                self.strings["monitoring_msg"].format(
                    chat_title,
                    chat_id,
                    sender_name,
                    link,
                    text,
                ),
                parse_mode="Markdown",
            )
            logger.debug(
                f"Sent notification about trigger word(s) {found_triggers} to chat {self._target_chat}"
            )
        except Exception as e:
            logger.error(f"Error processing message: {e}")
