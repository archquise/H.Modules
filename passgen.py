# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: PassgenMod
# Description: Generates random password
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/passgen.png
# ---------------------------------------------------------------------------------

import secrets
import string
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

def generate_password(
    length: int, letters: bool = True, numbers: bool = True, symbols: bool = True
) -> str:
    """Generates a random password with customizable options.

    Args:
        length: The desired length of the password.
        letters: Include lowercase and uppercase letters (default: True).
        numbers: Include digits (default: True).
        symbols: Include common symbols (default: True).

    Returns:
        A randomly generated password string.

    Raises:
        ValueError: If all character sets are disabled (letters, numbers, symbols).
    """
    character_sets = []
    if letters:
        character_sets.append(string.ascii_letters)
    if numbers:
        character_sets.append(string.digits)
    if symbols:
        character_sets.append(string.punctuation)

    if not character_sets:
        raise ValueError("At least one of letters, numbers, or symbols must be True")

    combined_characters = "".join(character_sets)
    password = "".join(secrets.choice(combined_characters) for _ in range(length))
    return password


@loader.tds
class PassgenMod(loader.Module):
    """generate random password"""

    strings = {
        "name": "Passgen",
        "pass": "<emoji document_id=5472287483318245416>*⃣</emoji> <b>Here is your secure password:</b> <code>{}</code>",
    }
    strings_ru = {
        "pass": "<emoji document_id=5472287483318245416>*⃣</emoji> <b>Вот ваш безопасный пароль:</b> <code>{}</code>"
    }

    @loader.command(
        ru_doc="Случайный пароль\n-n - цифры\n-s - символы \n -l - буквы",
        en_doc="Random password\n-n - numbers\n-s - symbols \n -l - letters",
    )
    async def password(self, message):
        """random password\n-n - numbers\n-s - symbols \n -l - letters"""
        text = message.text.split()
        length = 10
        letters = True
        numbers = False
        symbols = False
        for i in text:
            if i.startswith("password"):
                length = int(i.split("password")[1])
            elif i == "-n":
                numbers = True
            elif i == "-s":
                symbols = True
            elif i == "-l":
                letters = True
        password = generate_password(
            length=length, letters=letters, numbers=numbers, symbols=symbols
        )
        await utils.answer(message, self.strings("pass").format(password))
