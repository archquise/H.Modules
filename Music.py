# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: Music
# Description: Searches for music using Telegram music bots
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/Music.png
# ---------------------------------------------------------------------------------

# Thanks to @murpizz for the search code yandex

import logging

from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    FloodWaitError,
    MessageNotModifiedError,
)
from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class MusicMod(loader.Module):
    strings = {
        "name": "Music",
        "no_query": "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>Provide a search query!</b>",
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Searching...</b>",
        "found": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Possible match:</b>",
        "not_found": "<emoji document_id=5228947933545635555>😫</emoji> <b>Track not found: <code>{}</code></b>",
        "usage": "<b>Usage:</b> <code>.music [track name]</code>",
        "error": "<emoji document_id=5228947933545635555>⚠️</emoji> <b>Error:</b> <code>{}</code>",
        "no_results": "<emoji document_id=5228947933545635555>😫</emoji> <b>No results: <code>{}</code></b>",
        "flood_wait": "<emoji document_id=5462295343642956603>⏳</emoji> <b>Wait {}s (Telegram limits)</b>",
        "bot_error": "<emoji document_id=5228947933545635555>🤖</emoji> <b>Bot error: <code>{}</code></b>",
        "no_audio": "<emoji document_id=5228947933545635555>🎵</emoji> <b>No audio</b>",
        "generic_result": "<emoji document_id=5336965905773504919>ℹ️</emoji> <b>Non-media result. Check the bot's chat</b>",
        "yafind_searching": "<emoji document_id=5258396243666681152>🔎</emoji> <b>Searching Yandex.Music...</b>",
        "yafind_not_found": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Track not found on Yandex.Music</b>",
        "yafind_error": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Error (Yandex): {}</b>",
    }

    strings_ru = {
        "name": "Music",
        "no_query": "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>Укажите запрос!</b>",
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Поиск...</b>",
        "found": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Возможно, это оно:</b>",
        "not_found": "<emoji document_id=5228947933545635555>😫</emoji> <b>Трек не найден: <code>{}</code></b>",
        "usage": "<b>Использование:</b> <code>.music [название трека]</code>",
        "error": "<emoji document_id=5228947933545635555>⚠️</emoji> <b>Ошибка:</b> <code>{}</code>",
        "no_results": "<emoji document_id=5228947933545635555>😫</emoji> <b>Нет результатов: <code>{}</code></b>",
        "flood_wait": "<emoji document_id=5462295343642956603>⏳</emoji> <b>Подождите {}с (лимиты Telegram)</b>",
        "bot_error": "<emoji document_id=5228947933545635555>🤖</emoji> <b>Ошибка бота: <code>{}</code></b>",
        "no_audio": "<emoji document_id=5228947933545635555>🎵</emoji> <b>Нет аудио</b>",
        "generic_result": "<emoji document_id=5336965905773504919>ℹ️</emoji> <b>Немедийный результат. Проверьте чат с ботом</b>",
        "yafind_searching": "<emoji document_id=5258396243666681152>🔎</emoji> <b>Поиск в Яндекс.Музыке...</b>",
        "yafind_not_found": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Трек не найден в Яндекс.Музыке</b>",
        "yafind_error": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Ошибка (Яндекс): {}</b>",
    }

    def __init__(self):
        self.murglar_bot = "@murglar_bot"

    @loader.command(
        ru_doc="Найти трек в Yandex.Music: `.music {название}`",
        en_doc="Find a track in Yandex.Music: `.music {name}`",
    )
    async def music(self, message):
        args = utils.get_args(message)

        if not args:
            if reply := await message.get_reply_message():
                await self._yafind(message, reply.raw_text.strip())
            else:
                await utils.answer(message, self.strings("usage", message))
            return
            
        await self._yafind(message, query=args)

    async def _yafind(self, message: Message, query: str):
        if not query:
            return await utils.answer(message, self.strings("no_query", message))

        await utils.answer(message, self.strings("yafind_searching", message))

        try:
            results = await message.client.inline_query(
                self.murglar_bot, f"s:ynd {query}"
            )

            if not results:
                return await utils.answer(
                    message, self.strings("yafind_not_found", message)
                )

            await results[0].click(
                entity=message.chat_id,
                hide_via=True,
                reply_to=message.reply_to_msg_id if message.reply_to_msg_id else None,
            )
            await message.delete()

        except Exception as e:
            logger.exception("Yandex search error:")
            await utils.answer(message, self.strings("yafind_error", message).format(e))
