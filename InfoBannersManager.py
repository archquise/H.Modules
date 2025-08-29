# Proprietary License Agreement

# Copyright (c) 2024-29 Archquise

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

# 4. Any use of the Software must include the above copyright notice and this permission notice in all copies or substantial portions of the Software.

# 5. By using the Software, you agree to be bound by the terms and conditions of this license.

# For any inquiries or requests for permissions, please contact archquise@gmail.com.

# ---------------------------------------------------------------------------------
# Name: InfoBannersManager
# Description: Автоматически меняет баннеры на случайные из выбранного списка через заданный промежуток времени
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods

from .. import loader, utils

import logging
import random
import asyncio

logger = logging.getLogger(__name__)


@loader.tds
class InfoBannersManagerMod(loader.Module):
    """Автоматически меняет баннеры на случайные из выбранного списка через заданный промежуток времени"""

    strings = {"name": "InfoBannersManager"}

    def __init__(self):
        self.changer_instance = None
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "delay",
                60,
                "Задержка между изменениями баннеров в секундах",
                validator=loader.validators.Integer(minimum=1),
            ),
            loader.ConfigValue(
                "bannerslist",
                None,
                "Список ссылок на баннеры",
                validator=loader.validators.Series(validator=loader.validators.Link()),
            ),
        )

    async def banner_changer(self):
        while True:
            try:
                if not self.config["bannerslist"]:
                    logger.warning("Banners list is empty!")
                    await asyncio.sleep(10)
                    return

                banner = random.choice(self.config["bannerslist"])
                instance = self.lookup("HerokuInfo")
                if not instance:
                    instance = self.lookup("HikkaInfo")
                instance.config["banner_url"] = banner

            except Exception as e:
                logger.exception(f"Caught exception: {e}")
                await asyncio.sleep(10)
            await asyncio.sleep(self.config["delay"])

    async def on_unload(self):
        if self.changer_instance:
            self.changer_instance.cancel()
            self.changer_instance = None

    @loader.command(
        ru_doc="Включить или выключить модуль",
    )
    async def autobannertoggle(self, message):
        if not self.db.get(__name__, "enabled", False):
            try:
                if self.changer_instance:
                    self.changer_instance.cancel()

                self.db.set(__name__, "enabled", True)
                self.changer_instance = asyncio.create_task(self.banner_changer())
                await utils.answer(message, "Модуль запущен!")
            except Exception as e:
                logger.exception(f"Caught exception: {e}")
        else:
            try:
                self.db.set(__name__, "enabled", False)
                await utils.answer(message, "Модуль остановлен!")
                if self.changer_instance:
                    self.changer_instance.cancel()
                    self.changer_instance = None
            except Exception as e:
                logger.exception(f"Caught exception: {e}")
