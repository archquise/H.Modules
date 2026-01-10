# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: KBSwapper
# Description: KBSwapper is a module for changing the keyboard layout
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/KBSwapper.png
# ---------------------------------------------------------------------------------

import logging
import string

from .. import loader, utils

logger = logging.getLogger(__name__)

EN_TO_RU = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./`" + 'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~',
    "йцукенгшщзхъфывапролджэячсмитьбю.ё" + "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё",
)

RU_TO_EN = str.maketrans(
    "йцукенгшщзхъфывапролджэячсмитьбю.ё" + "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё",
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./`" + 'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~',
)


@loader.tds
class KBSwapperMod(loader.Module):
    """KBSwapper is a module for changing the keyboard layout"""

    strings = {
        "name": "KBSwapper",
        "no_reply": "<emoji document_id=5774077015388852135>❌</emoji> <b>Please reply to a message.</b>",
        "no_text": "<emoji document_id=5774077015388852135>❌</emoji> <b>The replied message does not contain text.</b>",
        "original_message": "<emoji document_id=5260450573768990626>➡️</emoji> <b>Original message:</b>\n<code>{original}</code>",
        "fixed_message": "<emoji document_id=5774022692642492953>✅</emoji> <b>Fixed message:</b>\n<code>{fixed}</code>",
        "error": "<emoji document_id=5774077015388852135>❌</emoji> <b>An error occurred while processing the message.</b>",
    }
    strings_ru = {
        "no_reply": "<emoji document_id=5774077015388852135>❌</emoji> <b>Пожалуйста, ответьте на сообщение.</b>",
        "no_text": "<emoji document_id=5774077015388852135>❌</emoji> <b>Отвеченное сообщение не содержит текста.</b>",
        "original_message": "<emoji document_id=5260450573768990626>➡️</emoji> <b>Оригинальное сообщение:</b>\n<code>{original}</code>",
        "fixed_message": "<emoji document_id=5774022692642492953>✅</emoji> <b>Исправленное сообщение:</b>\n<code>{fixed}</code>",
        "error": "<emoji document_id=5774077015388852135>❌</emoji> <b>Произошла ошибка при обработке сообщения.</b>",
    }

    @loader.command(
        ru_doc="При ответе на своё сообщение меняет раскладку путем редактирования, на чужое — в отдельном сообщении.",
        en_doc="Change keyboard layout for the replied message.",
    )
    async def swap(self, message):
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        original_text = reply.text
        if not original_text or original_text.isspace():
            await utils.answer(message, self.strings("no_text"))
            return

        try:
            trimmed_text = original_text.strip()

            has_russian = any(
                char
                in "йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ"
                for char in trimmed_text
            )
            has_english = any(char in string.ascii_letters for char in trimmed_text)

            logger.debug(
                f"Text analysis - Russian: {has_russian}, English: {has_english}, Text: {trimmed_text[:50]}..."
            )

            if has_russian and not has_english:
                fixed_text = original_text.translate(RU_TO_EN)
                logger.debug("Detected Russian text, translating to English")
            elif has_english and not has_russian:
                fixed_text = original_text.translate(EN_TO_RU)
                logger.debug("Detected English text, translating to Russian")
            else:
                first_char = (
                    trimmed_text[0].lower()
                    if trimmed_text
                    else original_text[0].lower()
                )
                logger.debug(
                    f"Mixed/other characters detected, first char: {first_char}"
                )
                if first_char in string.ascii_lowercase:
                    fixed_text = original_text.translate(EN_TO_RU)
                    logger.debug("Using first char detection: English to Russian")
                elif first_char in "йцукенгшщзхъфывапролджэячсмитьбюё":
                    fixed_text = original_text.translate(RU_TO_EN)
                    logger.debug("Using first char detection: Russian to English")
                else:
                    fixed_text = original_text
                    logger.debug("No recognizable letters, returning as is")

            if fixed_text != original_text:
                logger.debug(
                    f"Text changed: {original_text[:30]}... → {fixed_text[:30]}..."
                )
            else:
                logger.debug("Text unchanged")

            if message.sender_id == reply.sender_id:
                await reply.edit(fixed_text)
            else:
                await utils.answer(
                    message,
                    f"{self.strings('original_message').format(original=original_text)}\n"
                    f"{self.strings('fixed_message').format(fixed=fixed_text)}",
                )
        except Exception as e:
            logger.error(f"Error during swap: {e}")
            await utils.answer(message, self.strings("error"))
