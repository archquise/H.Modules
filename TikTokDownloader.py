# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: TikTokDownloader
# Description: A module for downloading videos and photos from TikTok without watermark
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/TikTokDownloader.png
# ---------------------------------------------------------------------------------

import asyncio
from dataclasses import dataclass
import logging
import os
import re
from typing import List, Optional, Union
from urllib.parse import urljoin

import aiohttp
from tqdm import tqdm

from .. import loader, utils

logger = logging.getLogger(__name__)


@dataclass
class data:
    dir_name: str
    media: Union[str, List[str]]
    type: str


class TikTok:
    def __init__(self, host: Optional[str] = None):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) "
                "AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 "
                "Mobile/7B334b Safari/531.21.10"
            )
        }
        self.host = host or "https://www.tikwm.com/"
        self.session = aiohttp.ClientSession()

        self.data_endpoint = "api"
        self.search_videos_keyword_endpoint = "api/feed/search"
        self.search_videos_hashtag_endpoint = "api/challenge/search"

        self.link = None
        self.result = None

        self.logger = logging.getLogger("damirtag-TikTok")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[damirtag-TikTok:%(funcName)s]: %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def close_session(self):
        await self.session.close()

    async def __ensure_data(self, link: str):
        if self.link != link:
            self.link = link
            self.result = await self._fetch_data(link)
            self.logger.info("Successfully ensured data from the link")

    async def __get_images(self, download_dir: Optional[str] = None):
        download_dir = download_dir or self.result["id"]
        os.makedirs(download_dir, exist_ok=True)

        tasks = [
            self._download_file(url, os.path.join(download_dir, f"image_{i + 1}.jpg"))
            for i, url in enumerate(self.result["images"])
        ]
        await asyncio.gather(*tasks)

        self.logger.info(f"Images - Downloaded and saved photos to {download_dir}")

        return data(
            dir_name=download_dir,
            media=[
                os.path.join(download_dir, f"image_{i + 1}.jpg")
                for i in range(len(self.result["images"]))
            ],
            type="images",
        )

    async def __get_video(self, video_filename: Optional[str] = None, hd: bool = False):
        video_url = self.result["hdplay"] if hd else self.result["play"]
        video_filename = video_filename or f"{self.result['id']}.mp4"

        async with self.session.get(video_url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            with open(video_filename, "wb") as file:
                with tqdm(
                    total=total_size, unit="B", unit_scale=True, desc=video_filename
                ) as pbar:
                    async for chunk in response.content.iter_any():
                        file.write(chunk)
                        pbar.update(len(chunk))

        self.logger.info(f"Video - Downloaded and saved video as {video_filename}")

        return data(
            dir_name=os.path.dirname(video_filename), media=video_filename, type="video"
        )

    async def _fetch_data(self, link: str) -> dict:
        url = self.get_url(link)
        params = {"url": url, "hd": 1}
        return await self._make_request(self.data_endpoint, params=params)

    async def _download_file(self, url: str, path: str):
        async with self.session.get(url) as response:
            response.raise_for_status()
            with open(path, "wb") as file:
                while chunk := await response.content.read(1024):
                    file.write(chunk)

    async def download_sound(
        self,
        link: str,
        audio_filename: Optional[str] = None,
        audio_ext: Optional[str] = ".mp3",
    ):
        await self.__ensure_data(link)

        if not audio_filename:
            audio_filename = f"{self.result['music_info']['title']}{audio_ext}"
        else:
            audio_filename += audio_ext

        await self._download_file(self.result["music_info"]["play"], audio_filename)
        self.logger.info(f"Sound - Downloaded and saved sound as {audio_filename}")
        return audio_filename

    async def download(
        self, link: str, video_filename: Optional[str] = None, hd: bool = True
    ):
        await self.__ensure_data(link)

        if "images" in self.result:
            return await self.__get_images(video_filename)

        if "hdplay" in self.result or "play" in self.result:
            return await self.__get_video(video_filename, hd)

        self.logger.error("No downloadable content found in the provided link.")
        raise Exception("No downloadable content found in the provided link.")

    async def _make_request(self, endpoint: str, params: dict) -> dict:
        async with self.session.get(
            urljoin(self.host, endpoint), params=params, headers=self.headers
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data.get("data", {})

    @staticmethod
    def get_url(text: str) -> Optional[str]:
        urls = re.findall(r"http[s]?://[^\s]+", text)
        return urls[0] if urls else None

    @staticmethod
    def _get_video_link(unique_id: str, aweme_id: str) -> str:
        return f"https://www.tiktok.com/@{unique_id}/video/{aweme_id}"

    @staticmethod
    def _get_uploader_link(unique_id: str) -> str:
        return f"https://www.tiktok.com/@{unique_id}"


@loader.tds
class TikTokDownloader(loader.Module):
    """TikTok Downloader module"""

    strings = {
        "name": "TikTokDownloader",
        "downloading": "<emoji document_id=5436024756610546212>⚡</emoji> <b>Downloading…</b>",
        "success_photo": "<emoji document_id=5436246187944460315>❤️</emoji> <b>The photo(s) has/have been successfully downloaded!</b>!",
        "success_video": "<emoji document_id=5436246187944460315>❤️</emoji> <b>The video has been successfully downloaded!</b>",
        "success_sound": "<emoji document_id=5436246187944460315>❤️</emoji> <b>The sound has been successfully downloaded!</b>",
        "error": "Error occurred while downloading.\n{}",
    }

    strings_ru = {
        "downloading": "<emoji document_id=5436024756610546212>⚡</emoji> <b>Загружаем…</b>",
        "success_photo": "<emoji document_id=5436246187944460315>❤️</emoji> <b>Фотография(-и) была(-и) успешно загружены!</b>!",
        "success_video": "<emoji document_id=5436246187944460315>❤️</emoji> <b>Видео было успешно загружено!</b>",
        "success_sound": "<emoji document_id=5436246187944460315>❤️</emoji> <b>Звук был успешно загружен!</b>",
        "error": "Во время загрузки произошла ошибка.\n{}",
    }

    @loader.command(
        ru_doc="Скачать звук с TikTok",
        en_doc="Download sound from TikTok",
    )
    async def ttsound(self, message):
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "Please provide a TikTok URL.")
            return

        url = args[0]
        await utils.answer(message, self.strings("downloading"))

        tiktok_downloader = TikTok()

        try:
            download_result = await tiktok_downloader.download_sound(url)
            await message.client.send_file(
                message.to_id, download_result, caption=self.strings("success_sound")
            )
            await message.delete()
        except Exception as e:
            await utils.answer(
                message,
                f"{self.strings('error').format(e)}\n Убедитесь, что ссылка ведет именно на видео или фото с нужным звуком, прямая ссылка на звук не сработает!",
            )
        finally:
            await tiktok_downloader.close_session()

    @loader.command(
        ru_doc="Скачать видео или фото с TikTok",
        en_doc="Download videos or photos from TikTok",
    )
    async def tt(self, message):
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "Please provide a TikTok URL.")
            return

        url = args[0]
        await utils.answer(message, self.strings("downloading"))

        tiktok_downloader = TikTok()

        try:
            download_result = await tiktok_downloader.download(url)

            if download_result.type == "video":
                await message.client.send_file(
                    message.to_id,
                    download_result.media,
                    caption=self.strings("success_video"),
                )
                await message.delete()
            elif download_result.type == "images":
                await message.client.send_file(
                    message.to_id,
                    download_result.media,
                    caption=self.strings("success_photo"),
                )
                await message.delete()

        except Exception as e:
            await utils.answer(message, self.strings("error").format(e))
        finally:
            await tiktok_downloader.close_session()
