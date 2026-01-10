# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: Жаконизатор
# Description: Жаконизатор
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# ---------------------------------------------------------------------------------

import io
import logging
from textwrap import wrap

import aiohttp
from PIL import Image, ImageDraw, ImageFont

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class JacquesMod(loader.Module):
    """Жаконизатор"""

    strings = {"name": "Жаконизатор", "usage": "Write <code>.help Жаконизатор</code>"}

    strings_ru = {"usage": "Напиши <code>.help Жаконизатор</code>"}

    def __init__(self):
        self.name = self.strings["name"]
        self._me = None
        self._ratelimit = []
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "font",
                "https://github.com/Codwizer/ReModules/blob/main/assets/OpenSans-Light.ttf?raw=true",
                lambda: "добавьте ссылку на нужный вам шрифт",
            ),
            loader.ConfigValue(
                "location",
                "center",
                "Можно указать left, right или center",
                validator=loader.validators.Choice(["left", "right", "center"]),
            ),
        )

    @loader.command(
        ru_doc="<реплай на сообщение/свой текст>",
        en_doc="<reply to the message/your own text>",
    )
    async def ionicmd(self, message):
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)

        if not args:
            if not reply:
                await utils.answer(message, self.strings("usage", message))
                return
            else:
                txt = reply.raw_text
        else:
            txt = args

        async with aiohttp.ClientSession() as session:
            async with session.get(self.config["font"]) as font_response:
                font_data = await font_response.read()

            async with session.get(
                "https://raw.githubusercontent.com/Codwizer/ReModules/main/assets/IMG_20231128_152538.jpg"
            ) as pic_response:
                pic_data = await pic_response.read()

        img = Image.open(io.BytesIO(pic_data)).convert("RGB")

        wrapped_text = "\n".join(wrap(txt, 19)) + "\n"
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(io.BytesIO(font_data), 32, encoding="UTF-8")

        text_size = draw.multiline_textsize(wrapped_text, font=font)
        imtext = Image.new("RGBA", (text_size[0] + 10, text_size[1] + 10), (0, 0, 0, 0))
        draw_imtext = ImageDraw.Draw(imtext)
        draw_imtext.multiline_text(
            (10, 10), wrapped_text, (0, 0, 0), font=font, align=self.config["location"]
        )

        imtext.thumbnail((350, 195))
        img.paste(imtext, (10, 10), imtext)

        out = io.BytesIO()
        out.name = "hikka_mods.jpg"
        img.save(out)
        out.seek(0)

        await message.client.send_file(message.to_id, out, reply_to=reply)
        await message.delete()
