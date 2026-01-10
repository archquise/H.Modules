# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: TelegramStatusCodes
# Description: Dictionary of telegram status codes
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/TelegramStatusCodes.png
# ---------------------------------------------------------------------------------

import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

responses = {
    300: (
        "⛔ SEE_OTHER",
        "The request must be repeated, but directed to a different data center.",
    ),
    400: (
        "⛔ BAD_REQUEST",
        "The query contains errors. In the event that a request was created using a form and contains user generated data, the user should be notified that the data must be corrected before the query is repeated.",
    ),
    401: (
        "⛔ UNAUTHORIZED",
        "There was an unauthorized attempt to use functionality available only to authorized users.",
    ),
    403: (
        "⛔ FORBIDDEN",
        "Privacy violation. For example, an attempt to write a message to someone who has blacklisted the current user.",
    ),
    404: (
        "⛔ NOT_FOUND",
        "An attempt to invoke a non-existent object, such as a method",
    ),
    406: (
        "⛔ NOT_ACCEPTABLE",
        """
Similar to <b>400 BAD_REQUESTS</b>, but the app must display the error to the user a bit differently.
Do not display any visible error to the user when receiving the <b>rpc_error</b> constructor: instead, wait for an <a href="https://core.telegram.org/constructor/updateServiceNotification ">updateServiceNotification</a> update, and handle it as usual.
Basically, an <a href="https://core.telegram.org/constructor/updateServiceNotification"updateServiceNotification</a> <b>pop-up</b> update will be emitted independently (ie NOT as an <a href="https://core.telegram.org/type/Updates">Updates</a> constructor inside <b>rpc_result</b> but as a normal update) immediately after emission of a 406 <b>rpc_error</b>: the update will contain the actual localized error message to show to the user with a UI popup.

An exception to this is the <b>AUTH_KEY_DUPLICATED</b> error, which is only emitted if any of the non-media DC detects that an authorized session is sending requests in parallel from two separate TCP connections, from the same or different IP addresses.
Note that parallel connections are still allowed and actually recommended for media DCs.
Also note that by session we mean a logged-in session identified by an <a href="https://core.telegram.org/constructor/authorization">authorization</a> constructor, fetchable using <a href="https://core.telegram.org/method/account.getAuthorizations">account.getAuthorizations</a>, not an MTProto session.

If the client receives an <b>AUTH_KEY_DUPLICATED</b> error, the session was already invalidated by the server and the user must generate a new auth key and login again.""",
    ),
    420: (
        "⛔ FLOOD",
        "The maximum allowed number of attempts to invoke the given method with the given input parameters has been exceeded. For example, in an attempt to request a large number of text messages (SMS) for the same phone number.",
    ),
    500: (
        "⛔ INTERNAL",
        """An internal server error occurred while a request was being processed; for example, there was a disruption while accessing a database or file storage.

If a client receives a 500 error, or you believe this error should not have occurred, please collect as much information as possible about the query and error and send it to the developers""",
    ),
}

responses_ru = {
    300: (
        "⛔ SEE_OTHER",
        "Запрос должен быть повторен, но направлен в другой дата-центр.",
    ),
    400: (
        "⛔ BAD_REQUEST",
        "Запрос содержит ошибки. В случае, если запрос был создан с помощью формы и содержит данные, введенные пользователем, пользователю следует сообщить, что данные должны быть исправлены перед повторным выполнением запроса.",
    ),
    401: (
        "⛔ UNAUTHORIZED",
        "Была совершена неавторизованная попытка использовать функциональность, доступную только авторизованным пользователям.",
    ),
    403: (
        "⛔ FORBIDDEN",
        "Нарушение конфиденциальности. Например, попытка написать сообщение пользователю, который добавил текущего пользователя в черный список.",
    ),
    404: (
        "⛔ NOT_FOUND",
        "Попытка обращения к несуществующему объекту, например, к методу.",
    ),
    406: (
        "⛔ NOT_ACCEPTABLE",
        """
Аналогично <b>400 BAD_REQUESTS</b>, но приложение должно отображать ошибку пользователю немного иначе.
Не показывайте пользователю видимую ошибку при получении конструктора <b>rpc_error</b>: вместо этого дождитесь обновления <a href="https://core.telegram.org/constructor/updateServiceNotification">updateServiceNotification</a> и обработайте его как обычно.
По сути, обновление-всплывающее окно <b>updateServiceNotification</b> будет отправлено независимо (т.е. НЕ как конструктор <b>Updates</b> внутри <b>rpc_result</b>, а как обычное обновление) сразу после выдачи 406 <b>rpc_error</b>: обновление будет содержать актуальное локализованное сообщение об ошибке для показа пользователю в интерфейсе.

Исключением является ошибка <b>AUTH_KEY_DUPLICATED</b>, которая возникает только в том случае, если любой из не-медиа DC обнаруживает, что авторизованная сессия отправляет запросы параллельно из двух отдельных TCP-соединений с одного или разных IP-адресов.
Обратите внимание, что параллельные соединения по-прежнему разрешены и фактически рекомендуются для медиа-DC.
Также обратите внимание, что под сессией понимается авторизованная сессия, идентифицируемая конструктором <a href="https://core.telegram.org/constructor/authorization">authorization</a>, которую можно получить с помощью <a href="https://core.telegram.org/method/account.getAuthorizations">account.getAuthorizations</a>, а не сессия MTProto.

Если клиент получает ошибку <b>AUTH_KEY_DUPLICATED</b>, сессия уже была аннулирована сервером, и пользователю необходимо сгенерировать новый ключ авторизации и войти снова.""",
    ),
    420: (
        "⛔ FLOOD",
        "Превышено максимально допустимое количество попыток вызова данного метода с указанными входными параметрами. Например, при попытке запросить большое количество текстовых сообщений (SMS) для одного и того же номера телефона.",
    ),
    500: (
        "⛔ INTERNAL",
        """Произошла внутренняя ошибка сервера во время обработки запроса; например, произошел сбой при доступе к базе данных или файловому хранилищу.

Если клиент получает ошибку 500 или вы считаете, что эта ошибка не должна была возникнуть, пожалуйста, соберите как можно больше информации о запросе и ошибке и отправьте ее разработчикам.""",
    ),
}


@loader.tds
class TelegramStatusCodes(loader.Module):
    """Dictionary of telegram status codes"""

    strings = {
        "name": "TelegramStatusCodes",
        "args_incorrect": "<b>Incorrect args</b>",
        "not_found": "<b>Code not found</b>",
        "syntax_error": "<b>Args are mandatory</b>",
        "scode": "<b>{} {}</b>\n⚜️ Code Description: <i>{}</i>",
    }

    strings_ru = {
        "args_incorrect": "<b>Неверные аргументы</b>",
        "not_found": "<b>Код не найден</b>",
        "syntax_error": "<b>Аргументы обязательны</b>",
        "_cmd_doc_httpsc": "<код> - Получить информацию о статус-коде",
        "_cmd_doc_httpscs": "Показать все доступные коды",
        "_cls_doc": "Словарь статус-кодов Telegram",
        "scode": "<b>{} {}</b>\n⚜️ Описание статус-кода: <i>{}</i>",
    }

    async def client_ready(self, client, db):
        self.ub_lang = self._db.get("hikka.translations", "lang")
        if not self.ub_lang:
            self.ub_lang = self._db.get("heroku.translations", "lang")

    @loader.unrestricted
    @loader.command(
        ru_doc="<код состояния> - Получение информации о статус-коде",
        en_doc="<statuscode> - Get status code info",
    )
    async def tgccmd(self, message):

        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("syntax_error", message))
            return

        try:
            if int(args[0]) not in responses:
                await utils.answer(message, self.strings("not_found", message))
        except ValueError:
            await utils.answer(message, self.strings("args_incorrect", message))

        if self.ub_lang != "ru":
            await utils.answer(
                message,
                self.strings("scode", message).format(
                    responses[int(args[0])][0], args[0], responses[int(args[0])][1]
                ),
            )
        else:
            await utils.answer(
                message,
                self.strings("scode", message).format(
                    responses[int(args[0])][0], args[0], responses_ru[int(args[0])][1]
                ),
            )


    @loader.unrestricted
    @loader.command(
        ru_doc="Получите все статус-коды Telegram",
        en_doc="Get all Telegram status codes",
    )
    async def tgcscmd(self, message):
        await utils.answer(
            message,
            "\n".join(
                [f"<b>{str(sc)}: {text}</b>" for sc, (text, _) in responses.items()]
            ),
        )
