# ###########█▄█   █▀▄▀█ █▀█ █▀▄ █▀###########
# ###########█ █ ▄ █ ▀ █ █▄█ █▄▀ ▄█###########

# ##### Copyright (c) 2024-2029 CodWiz #######

# 💬 Contact: https://t.me/shuseks
# 🔒 Licensed under custom proprietary license.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/H.Modules/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: TelegraphComics
# Description: Create comics on Telegraph from ZIP/RAR archives
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# meta banner: https://raw.githubusercontent.com/archquise/hmods_meta/main/TelegraphComics.png
# requires: aiohttp, zipfile, telegraph
# ---------------------------------------------------------------------------------

import asyncio
import logging
import os
import re
import tempfile
from typing import List, Optional
import zipfile
import html

import aiohttp
from telethon.types import MessageMediaDocument

from telegraph import Telegraph

from .. import loader, utils

logger = logging.getLogger(__name__)


class FileUploader:
    """Class for handling file uploads to various hosting services"""

    def __init__(self, config):
        self.config = config

    async def _upload_file_to_service(
        self,
        session: aiohttp.ClientSession,
        url: str,
        file_path: str,
        field_name: str,
        **extra_fields,
    ) -> Optional[str]:
        """Generic file upload method"""
        try:
            with open(file_path, "rb") as f:
                data = aiohttp.FormData()
                data.add_field(field_name, f, filename=os.path.basename(file_path))

                for key, value in extra_fields.items():
                    data.add_field(key, value)

                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        return result.strip() if result else None
                    else:
                        logger.info(
                            f"Upload failed with status {response.status}: {await response.text()}"
                        )
        except Exception as e:
            logger.info(f"Error uploading to {url}: {e}")
        return None

    async def upload_to_catbox(self, file_path: str) -> Optional[str]:
        """Upload file to catbox.moe"""
        async with aiohttp.ClientSession() as session:
            result = await self._upload_file_to_service(
                session,
                "https://catbox.moe/user/api.php",
                file_path,
                "fileToUpload",
                reqtype="fileupload",
            )
            return (
                result
                if result and result.startswith("https://files.catbox.moe/")
                else None
            )

    async def upload_to_bashupload(self, file_path: str) -> Optional[str]:
        """Upload file to bashupload.com"""
        async with aiohttp.ClientSession() as session:
            try:
                with open(file_path, "rb") as f:
                    data = aiohttp.FormData()
                    data.add_field("file", f, filename=os.path.basename(file_path))

                    async with session.post(
                        "https://bashupload.com", data=data
                    ) as response:
                        if response.status == 200:
                            result = await response.text()

                            lines = result.strip().split("\n")
                            for line in lines:
                                if line.startswith("https://"):
                                    return line

                            if "wget" in result:
                                urls = [
                                    line
                                    for line in result.split("\n")
                                    if "wget" in line
                                ]
                                if urls:
                                    parts = urls[0].split()
                                    for part in parts:
                                        if part.startswith("https://"):
                                            return part
            except Exception as e:
                logger.info(f"Error uploading to bashupload: {e}")
        return None

    async def upload_to_kappa(self, file_path: str) -> Optional[str]:
        """Upload file to kappa.lol"""
        async with aiohttp.ClientSession() as session:
            try:
                with open(file_path, "rb") as f:
                    data = aiohttp.FormData()
                    data.add_field("file", f, filename=os.path.basename(file_path))

                    async with session.post(
                        "https://kappa.lol/api/upload", data=data
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            if result and "id" in result:
                                return f"https://kappa.lol/{result['id']}"
            except Exception as e:
                logger.info(f"Error uploading to kappa: {e}")
        return None

    async def upload_to_pomf(self, file_path: str) -> Optional[str]:
        """Upload file to pomf.lain.la"""
        async with aiohttp.ClientSession() as session:
            try:
                with open(file_path, "rb") as f:
                    data = aiohttp.FormData()
                    data.add_field("files[]", f, filename=os.path.basename(file_path))

                    async with session.post(
                        "https://pomf.lain.la/upload.php", data=data
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            if result and "files" in result and result["files"]:
                                return result["files"][0].get("url")
            except Exception as e:
                logger.info(f"Error uploading to pomf: {e}")
        return None

    async def upload_file(self, file_path: str) -> Optional[str]:
        """Upload file to selected service"""
        service_name = self.config["upload_service"]

        service_map = {
            "catbox": self.upload_to_catbox,
            "bashupload": self.upload_to_bashupload,
            "kappa": self.upload_to_kappa,
            "pomf": self.upload_to_pomf,
        }

        service_func = service_map.get(service_name)
        if not service_func:
            return await self.upload_to_catbox(file_path)

        try:
            result = await service_func(file_path)
            return result
        except Exception as e:
            logger.error(f"Upload to {service_name} failed: {e}")
            return None


@loader.tds
class TelegraphComicMod(loader.Module):
    """Create comics on Telegraph from ZIP/CBZ/RAR archives"""

    strings = {
        "name": "TelegraphComic",
        "invalid_args": "<emoji document_id=5388785832956016892>❌</emoji> Invalid arguments. Usage: .telegraphcomics <title> | <cover_url> (optional)",
        "no_reply": "<emoji document_id=5388785832956016892>❌</emoji> Reply to a message with ZIP/CBZ/RAR file",
        "unsupported_format": "<emoji document_id=5388785832956016892>❌</emoji> Unsupported file format. Only ZIP/CBZ/RAR files are supported",
        "processing": "<emoji document_id=5256094480498436162>⏳</emoji> Processing archive...",
        "uploading": "<emoji document_id=5854762571659218443>⏳</emoji> Uploading images...",
        "creating_article": "<emoji document_id=5854762571659218443>⏳</emoji> Creating Telegraph article...",
        "archive_extracted": "<emoji document_id=5854762571659218443>📦</emoji> Archive successfully extracted: <emoji document_id=5208422125924275090>✅</emoji>",
        "upload_files": "<emoji document_id=5854762571659218443>📦</emoji> Upload image files:",
        "creating_telegraph": "<emoji document_id=5854762571659218443>📝</emoji> Creating Telegraph article:",
        "success": '<emoji document_id=5208422125924275090>✅</emoji> <b>Telegraph article created!</b>\n\n<emoji document_id=5256094480498436162>📦</emoji> Archive successfully extracted: <emoji document_id=5208422125924275090>✅</emoji>\n\n<emoji document_id=5256094480498436162>📦</emoji> Upload image files:\n{upload_status}\n\n<emoji document_id=5256230583717079814>📝</emoji> Creating Telegraph article:\n{article_status}\n\n<emoji document_id=5271604874419647061>🔗</emoji> <a href="{url}">{url}</a>',
        "error": "<emoji document_id=5854929766146118183>❌</emoji> <b>Error:</b> {}",
        "_cls_doc": "Create comics on Telegraph from ZIP/CBZ/RAR archives",
    }

    strings_ru = {
        "_cls_doc": "Создание комиксов на Telegraph из ZIP/CBZ/RAR архивов",
        "invalid_args": "<emoji document_id=5388785832956016892>❌</emoji> Неверные аргументы. Использование: .telegraphcomics <название> | <ссылка_на_обложку>(необязательно)",
        "no_reply": "<emoji document_id=5388785832956016892>❌</emoji> Ответьте на сообщение с ZIP/CBZ/RAR файлом",
        "unsupported_format": "<emoji document_id=5388785832956016892>❌</emoji> Неподдерживаемый формат. Только ZIP/CBZ/RAR файлы",
        "processing": "<emoji document_id=5256094480498436162>⏳</emoji> Обработка архива...",
        "uploading": "<emoji document_id=5256094480498436162>⏳</emoji> Загрузка изображений...",
        "creating_article": "<emoji document_id=5854762571659218443>⏳</emoji> Создание Telegraph статьи...",
        "archive_extracted": "<emoji document_id=5256094480498436162>📦</emoji> Архив успешно распакован: <emoji document_id=5208422125924275090>✅</emoji>",
        "upload_files": "<emoji document_id=5256094480498436162>📦</emoji> Загрузка файлов изображений:",
        "creating_telegraph": "<emoji document_id=5854762571659218443>📝</emoji> Создание Telegraph статьи:",
        "success": '<emoji document_id=5208422125924275090>✅</emoji> <b>Telegraph статья создана!</b>\n\n<emoji document_id=5256094480498436162>📦</emoji> Архив успешно распакован: <emoji document_id=5208422125924275090>✅</emoji>\n\n<emoji document_id=5256094480498436162>📦</emoji> Загрузка файлов изображений:\n{upload_status}\n\n<emoji document_id=5256230583717079814>📝</emoji> Создание Telegraph статьи:\n{article_status}\n\n<emoji document_id=5271604874419647061>🔗</emoji> <a href="{url}">{url}</a>',
        "error": "<emoji document_id=5388785832956016892>❌</emoji> <b>Ошибка:</b> {}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "upload_service",
                "catbox",
                "Upload service to use",
                validator=loader.validators.Choice(
                    ["catbox", "bashupload", "kappa", "pomf"]
                ),
            ),
            loader.ConfigValue(
                "short_name",
                "HikkaMods",
                "short name for the article",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "author_name",
                "HikkaMods",
                "nickname of the author of the article",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "author_url",
                "https://t.me/hikka_mods",
                "link to author",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "header_text",
                None,
                "Text to add at the beginning of the article (set to null to disable)",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "smart_sorting",
                True,
                "Enable smart file numbering (supports both 001 and 1 formats)",
                validator=loader.validators.Boolean(),
            ),
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.uploader = FileUploader(self.config)
        self.telegraph = Telegraph()
        self.telegraph.create_account(
            short_name=self.config["short_name"],
            author_name=self.config["author_name"],
            author_url=self.config["author_url"],
        )

    def _extract_number_from_filename(self, filename: str) -> tuple:
        """Extract number from filename for smart sorting with HTML support"""

        try:
            decoded_filename = html.unescape(filename)
        except Exception:
            decoded_filename = filename

        match = re.search(r"(\d+)", decoded_filename)
        if match:
            return int(match.group(1)), filename
        return float("inf"), filename

    async def extract_zip_archive(self, zip_path: str, extract_dir: str) -> List[str]:
        """Extract ZIP archive and return sorted list of image files"""
        image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".avif"}
        image_files = []

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

                for root, _, files in os.walk(extract_dir):
                    for file in files:
                        if os.path.splitext(file)[1].lower() in image_extensions:
                            image_files.append(os.path.join(root, file))

                if self.config["smart_sorting"]:
                    image_files.sort(
                        key=lambda x: self._extract_number_from_filename(
                            os.path.basename(x)
                        )
                    )
                else:
                    image_files.sort(key=lambda x: os.path.basename(x).lower())

        except Exception as e:
            logger.info(f"Error extracting ZIP archive: {e}")

        return image_files

    async def create_telegraph_article(
        self, title: str, image_urls: List[str], cover_url: Optional[str] = None
    ) -> Optional[str]:
        """Create Telegraph article with images"""
        try:
            content_parts = []

            header_text = self.config["header_text"]
            if header_text:
                content_parts.append(f"<p>{header_text}</p><br>")

            if cover_url:
                content_parts.append(f'<img src="{cover_url}"/><br>')

            content_parts.extend(f'<img src="{url}"/>' for url in image_urls)

            content = "".join(content_parts)

            response = await asyncio.to_thread(
                lambda: self.telegraph.create_page(
                    title=title,
                    html_content=content,
                    author_name=self.config["author_name"],
                    author_url=self.config["author_url"],
                )
            )

            return response["url"]

        except Exception as e:
            logger.info(f"Error creating Telegraph article: {e}")
            return None

    async def _process_cover_url(self, cover_url: str) -> Optional[str]:
        """Process cover URL - handle Telegram message links and direct URLs"""
        if not cover_url:
            return None

        cover_url = cover_url.strip()

        if "t.me/" in cover_url and "/" in cover_url.split("t.me/")[1]:
            try:
                parts = cover_url.split("/")
                if len(parts) >= 4:
                    chat_username = parts[-3]
                    message_id = int(parts[-1])

                    message = await self.client.get_messages(
                        chat_username, ids=message_id
                    )
                    if message and message.media:
                        media_path = await message.download_media()
                        if media_path:
                            uploaded_url = await self.uploader.upload_file(media_path)
                            os.remove(media_path)
                            return uploaded_url
            except Exception as e:
                logger.info(f"Error processing Telegram cover link: {e}")
                return cover_url

        return cover_url

    async def _process_comics_request(self, message, create_func) -> None:
        """Common logic for processing comics requests"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args or not reply:
            await utils.answer(message, self.strings["invalid_args"])
            return

        if not isinstance(reply.media, MessageMediaDocument):
            await utils.answer(message, self.strings["no_reply"])
            return

        if "|" in args:
            title, cover_url = args.split("|", 1)
        else:
            title = args
            cover_url = None

        title = title.strip()
        cover_url = (
            await self._process_cover_url(cover_url.strip()) if cover_url else None
        )

        await utils.answer(message, self.strings["processing"])

        file_path = await reply.download_media()
        if not file_path:
            await utils.answer(
                message, self.strings["error"].format("Failed to download file")
            )
            return

        try:
            if not (file_path.lower().endswith((".zip", ".cbz"))):
                await utils.answer(message, self.strings["unsupported_format"])
                return

            with tempfile.TemporaryDirectory() as temp_dir:
                archive_path = file_path
                if file_path.lower().endswith(".cbz"):
                    import shutil

                    zip_path = file_path[:-4] + ".zip"
                    shutil.copy2(file_path, zip_path)
                    archive_path = zip_path

                image_files = await self.extract_zip_archive(archive_path, temp_dir)

                if archive_path != file_path and os.path.exists(archive_path):
                    os.remove(archive_path)
                if not image_files:
                    await utils.answer(
                        message,
                        self.strings["error"].format("No images found in archive"),
                    )
                    return

                await utils.answer(message, self.strings["archive_extracted"])

                await utils.answer(message, self.strings["uploading"])

                upload_tasks = [
                    self.uploader.upload_file(img_file) for img_file in image_files
                ]
                upload_results = await asyncio.gather(
                    *upload_tasks, return_exceptions=True
                )
                image_urls = []
                failed_uploads = 0
                upload_errors = []
                upload_status_lines = []

                for i, (img_file, result) in enumerate(
                    zip(image_files, upload_results)
                ):
                    filename = os.path.basename(img_file)
                    if isinstance(result, Exception):
                        error_str = str(result)
                        logger.info(f"Upload failed: {error_str}")
                        failed_uploads += 1
                        upload_errors.append(error_str)
                        upload_status_lines.append(
                            f"{filename} - <emoji document_id=5388785832956016892>❌</emoji>"
                        )
                    elif result and "https://" in result:
                        image_urls.append(result)
                        upload_status_lines.append(
                            f"{filename} - <emoji document_id=5208422125924275090>✅</emoji>"
                        )
                    else:
                        failed_uploads += 1
                        upload_errors.append("Invalid response from upload service")
                        upload_status_lines.append(
                            f"{filename} - <emoji document_id=5388785832956016892>❌</emoji>"
                        )

                if not image_urls:
                    error_details = []
                    error_details.append(f"Failed uploads: {failed_uploads}")

                    if upload_errors:
                        unique_errors = list(set(upload_errors))[:3]
                        error_details.append("Errors: " + "; ".join(unique_errors))

                    error_msg = " | ".join(error_details)
                    await utils.answer(
                        message,
                        self.strings["error"].format(error_msg),
                    )
                    return

                upload_status = (
                    self.strings["upload_files"] + "\n" + "\n".join(upload_status_lines)
                )
                await utils.answer(message, upload_status)

                await utils.answer(message, self.strings["creating_article"])

                article_url = await create_func(title, image_urls, cover_url)
                if article_url:
                    article_status_lines = []
                    for i, (img_file, url) in enumerate(zip(image_files, image_urls)):
                        filename = os.path.basename(img_file)
                        article_status_lines.append(
                            f"{filename} - <emoji document_id=5208422125924275090>✅</emoji>"
                        )

                    upload_status = "\n".join(upload_status_lines)
                    article_status = "\n".join(article_status_lines)

                    await utils.answer(
                        message,
                        self.strings["success"].format(
                            upload_status=upload_status,
                            article_status=article_status,
                            url=article_url,
                        ),
                    )

                else:
                    await utils.answer(
                        message,
                        self.strings["error"].format("Failed to create article"),
                    )
        except Exception as e:
            await utils.answer(
                message,
                self.strings["error"].format(f"Processing error: {e}"),
            )
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    @loader.command(
        ru_doc="Создать комикс на Telegraph из ZIP/CBZ/RAR архива\nАргументы: <название> | <ссылка_на_обложку>(необязательно)\nИспользование: .telegraphcomics <title> | <cover_url>(optional)",
        en_doc="Create Telegraph comic from ZIP/CBZ/RAR archive\nArguments: <title> | <cover_url>(optional)\nUsage: .telegraphcomics <title> | <cover_url>(optional)",
    )
    async def telegraphcomicscmd(self, message):
        await self._process_comics_request(message, self.create_telegraph_article)
