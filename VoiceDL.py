# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: VoiceDL
# Description: Voice Downloader module
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/VoiceDL.png
# requires: tempfile
# ---------------------------------------------------------------------------------

import asyncio
import logging
import os
import shutil
import tempfile

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class VoiceDLMod(loader.Module):
    """Download voice messages as MP3"""

    strings = {
        "name": "VoiceDL",
        "success": "✅ Voice downloaded as MP3",
        "error": "❌ Error downloading voice",
        "no_voice": "❌ Reply to a voice message",
        "no_ffmpeg": "❌ FFmpeg not found. Install: apt install ffmpeg",
    }

    strings_ru = {
        "success": "✅ Голосовое скачано как MP3",
        "error": "❌ Ошибка скачивания",
        "no_voice": "❌ Ответьте на голосовое",
        "no_ffmpeg": "❌ FFmpeg не установлен. Установите: apt install ffmpeg",
    }

    def __init__(self):
        self._ffmpeg_check = None

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        self._ffmpeg_check = shutil.which("ffmpeg") is not None

    @loader.command(
        ru_doc="[ответ] - скачать голосовое как MP3",
        en_doc="[reply] - download voice as MP3",
    )
    async def voicedl(self, message):
        if not self._ffmpeg_check:
            return await utils.answer(message, self.strings["no_ffmpeg"])

        reply = await message.get_reply_message()
        if not reply or not reply.voice:
            return await utils.answer(message, self.strings["no_voice"])

        await self._process_voice(message, reply)

    async def _process_voice(self, message, reply):
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                ogg_path = os.path.join(tmpdir, "voice.ogg")
                mp3_path = os.path.join(tmpdir, "voice.mp3")

                await reply.download_media(file=ogg_path)

                proc = await asyncio.create_subprocess_exec(
                    "ffmpeg",
                    "-i",
                    ogg_path,
                    "-codec:a",
                    "libmp3lame",
                    "-q:a",
                    "2",
                    mp3_path,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await proc.communicate()

                if proc.returncode != 0:
                    raise Exception("FFmpeg error")

                await message.client.send_file(
                    message.chat.id,
                    mp3_path,
                    caption=self.strings["success"],
                    reply_to=reply.id,
                )

            except Exception:
                await utils.answer(message, self.strings["error"])
