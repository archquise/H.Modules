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
                validator=loader.validators.Series(validator=loader.validators.Link())
            ),
        )

    async def banner_changer(self):
        while True:
            try:
                if not self.config['bannerslist']:
                    logger.warning('Banners list is empty!')
                    await asyncio.sleep(10)
                    return
                
                banner = random.choice(self.config['bannerslist'])
                instance = self.lookup('HerokuInfo')
                instance.config['banner_url'] = banner
                
            except Exception as e:
                logger.exception(f'Caught exception: {e}')
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
        if not self.db.get(__name__, 'enabled', False):
            try:
                if self.changer_instance:
                    self.changer_instance.cancel()
            
                self.db.set(__name__, 'enabled', True)
                self.changer_instance = asyncio.create_task(self.banner_changer())
                await utils.answer(message, 'Модуль запущен!')
            except Exception as e:
                logger.exception(f'Caught exception: {e}')
        else:
            try:
                self.db.set(__name__, 'enabled', False)
                await utils.answer(message, 'Модуль остановлен!')
                if self.changer_instance:
                    self.changer_instance.cancel()
                    self.changer_instance = None 
            except Exception as e:
                logger.exception(f'Caught exception: {e}')