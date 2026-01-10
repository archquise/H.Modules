# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: FakeActions
# Description: Module for simulating various actions in chat
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# ---------------------------------------------------------------------------------

import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class FakeActionsMod(loader.Module):
    """Module for simulating various actions in chat"""

    strings = {"name": "FakeActions"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "DEFAULT_DURATION", 5, "Default duration for actions in seconds"
        )

    async def ftcmd(self, message):
        """<seconds> - Simulates typing in chat for the specified number of seconds."""
        await self._simulate_action_command(message, "typing")

    async def ffcmd(self, message):
        """<seconds> - Simulates sending a file."""
        await self._simulate_action_command(message, "document")

    async def fgcmd(self, message):
        """<seconds> - Simulates recording a voice message."""
        await self._simulate_action_command(message, "record-audio")

    async def fvgcmd(self, message):
        """<seconds> - Simulates recording a video message."""
        await self._simulate_action_command(message, "record-round")

    async def fpgcmd(self, message):
        """<seconds> - Simulates playing a game."""
        await self._simulate_action_command(message, "game")

    async def _simulate_action_command(self, message, action):
        """General function for handling action simulation commands."""
        duration = self._parse_duration(message)
        if duration is None:
            await utils.answer(
                message,
                f"Usage: {self.get_prefix()}{message.raw_text.split()[0][1:]} <seconds>",
            )
            return

        await message.delete()
        await self._simulate_action(message, action, duration)

    def _parse_duration(self, message):
        """Parse the duration from the message."""
        args = message.raw_text.split()
        if len(args) == 2 and args[1].isdigit():
            return int(args[1])
        return self.config["DEFAULT_DURATION"]

    async def _simulate_action(self, message, action, duration):
        """Simulate the specified action in chat."""
        async with message.client.action(message.chat_id, action):
            await asyncio.sleep(duration)
