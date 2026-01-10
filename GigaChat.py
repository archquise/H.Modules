# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: GigaChat
# Description: Module for using GigaChat
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/GigaChat.png
# ---------------------------------------------------------------------------------

import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class GigaChatMod(loader.Module):
    """Module for using GigaChat"""

    strings = {
        "name": "GigaChat",
        "api_key_missing": "Please set the API key in the module configuration.",
        "query_missing": "Please enter a query after the command.",
        "response_error": "Failed to get a response from GigaChat.",
        "error_occurred": "An error occurred: {}",
        "formatted_response": (
            "<emoji document_id=6030848053177486888>❓</emoji> Query: {}\n"
            "<emoji document_id=6030400221232501136>🤖</emoji> GigaChat: {}"
        ),
        "giga_model": "List of GigaChat models:\n{}",
    }

    strings_ru = {
        "api_key_missing": "Пожалуйста, установите API ключ в конфигурации модуля.",
        "query_missing": "Пожалуйста, введите запрос после команды.",
        "response_error": "Не удалось получить ответ от GigaChat.",
        "error_occurred": "Произошла ошибка: {}",
        "formatted_response": (
            "<emoji document_id=6030848053177486888>❓</emoji> Запрос: {}\n"
            "<emoji document_id=6030400221232501136>🤖</emoji> GigaChat: {}"
        ),
        "giga_model": "Список моделей GigaChat:\n{}",
    }

    async def client_ready(self, client, db):
        self.hmodslib = await self.import_lib(
            "https://files.archquise.ru/HModsLibrary.py"
        )

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "GIGACHAT_API_KEY",
                None,
                "Введите ваш API ключ для GigaChat, Чтобы получить ключ API, перейдите сюда: https://developers.sber.ru/studio/workspaces",
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "GIGACHAT_MODEL",
                "GigaChat",
                "Введите модель, ее можно получить при команде .gigamodel",
            ),
        )

    @loader.command(
        ru_doc="Получите исчерпывающий ответ на свой вопрос",
        en_doc="Get GigaResponse to your question",
    )
    async def giga(self, message):
        api_key = self.config["GIGACHAT_API_KEY"]
        if not api_key:
            return await utils.answer(message, self.strings("api_key_missing"))

        query = utils.get_args_raw(message)
        if not query:
            return await utils.answer(message, self.strings("query_missing"))

        try:
            response = await self.hmodslib.get_giga_response(api_key, query)
            if response:
                await utils.answer(
                    message, self.strings("formatted_response").format(query, response)
                )
            else:
                await utils.answer(message, self.strings("response_error"))
        except Exception as e:
            await utils.answer(message, self.strings("error_occurred").format(str(e)))

    @loader.command(
        ru_doc="Получить список моделей",
        en_doc="Get a list of models",
    )
    async def gigamodel(self, message):
        api_key = self.config["GIGACHAT_API_KEY"]
        if not api_key:
            return await utils.answer(message, self.strings("api_key_missing"))

        try:
            response = await self.hmodslib.get_giga_models(api_key)
            if response:
                await utils.answer(message, self.strings("giga_model").format(response))
            else:
                await utils.answer(message, self.strings("response_error"))
        except Exception as e:
            await utils.answer(message, self.strings("error_occurred").format(str(e)))
