import asyncio
import os
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

from telethon import functions, types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import SendMediaRequest

from . import *

if not os.path.isdir("./temp"):
    os.makedirs("./temp")


@Andencento.on(andencento_cmd(pattern="stoi$"))
@Andencento.on(sudo_cmd(pattern="stoi$", allow_sudo=True))
async def _(user):
    if user.fwd_from:
        return
    reply_to_id = user.message.id
    if user.reply_to_msg_id:
        reply_to_id = user.reply_to_msg_id
    event = await eor(user, "Converting.....")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.jpg"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await user.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await user.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await eod(event, "Can't Convert")
    else:
        await event.edit(f"Syntax : `{hl}stoi` reply to a Telegram normal sticker")


@Andencento.on(andencento_cmd(pattern="itos$"))
@Andencento.on(sudo_cmd(pattern="itos$", allow_sudo=True))
async def _(user):
    if user.fwd_from:
        return
    reply_to_id = user.message.id
    if user.reply_to_msg_id:
        reply_to_id = user.reply_to_msg_id
    event = await eor(user, "Converting.....")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.webp"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await user.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await user.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await eod(event, "Can't Convert")
    else:
        await event.edit(f"Syntax : `{hl}itos` reply to a Telegram normal sticker")


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


@Andencento.on(andencento_cmd(pattern="ttf ?(.*)"))
@Andencento.on(sudo_cmd(pattern="ttf ?(.*)", allow_sudo=True))
async def get(event):
    if event.fwd_from:
        return
    name = event.text[5:]
    if name is None:
        await eod(event, f"reply to text message as `{hl}ttf <file name>`")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await eod(event, f"Reply to text message as `{hl}ttf <file name>`")


@Andencento.on(andencento_cmd(pattern="ftoi$"))
@Andencento.on(sudo_cmd(pattern="ftoi$", allow_sudo=True))
async def on_file_to_photo(event):
    if event.fwd_from:
        return
    target = await event.get_reply_message()
    hbot = await eor(event, "Converting.....")
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith("image/"):
        return  # This isn't an image
    if image.mime_type == "image/webp":
        return  # Telegram doesn't let you directly send stickers as photos
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise
    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = "image.png"
    try:
        await event.client(
            SendMediaRequest(
                peer=await event.get_input_chat(),
                media=types.InputMediaUploadedPhoto(img),
                message=target.message,
                entities=target.entities,
                reply_to_msg_id=target.id,
            )
        )
    except PhotoInvalidDimensionsError:
        return
    await hbot.delete()


@Andencento.on(andencento_cmd(pattern="gif$"))
@Andencento.on(sudo_cmd(pattern="gif$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    userreply = await event.get_reply_message()
    if not userreply or not userreply.media or not userreply.media.document:
        return await edit_or_reply(event, "`Stupid!, This is not animated sticker.`")
    if userreply.media.document.mime_type != "application/x-tgsticker":
        return await edit_or_reply(event, "`Stupid!, This is not animated sticker.`")
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@tgstogifbot"
    userevent = await edit_or_reply(event, "`Converting to gif ...`")
    async with bot.conversation(chat) as conv:
        try:
            await silently_send_message(conv, "/start")
            await bot.send_file(chat, userreply.media)
            response = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
            if response.text.startswith("Send me an animated sticker!"):
                return await userevent.edit("`This file is not supported`")
            userresponse = response if response.media else await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
            userfile = Path(await event.client.download_media(userresponse, "./temp/"))
            usergif = Path(await unzip(userfile))
            kraken = await bot.send_file(
                event.chat_id,
                usergif,
                support_streaming=True,
                force_document=False,
                reply_to=reply_to_id,
            )
            await bot(
                functions.messages.SaveGifRequest(
                    id=types.InputDocument(
                        id=kraken.media.document.id,
                        access_hash=kraken.media.document.access_hash,
                        file_reference=kraken.media.document.file_reference,
                    ),
                    unsave=True,
                )
            )
            await userevent.delete()
            for files in (usergif, userfile):
                if files and os.path.exists(files):
                    os.remove(files)
        except YouBlockedUserError:
            await userevent.edit("Unblock @tgstogifbot")
            return


@Andencento.on(andencento_cmd(pattern="nfc ?(.*)"))
@Andencento.on(sudo_cmd(pattern="nfc ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eod(event, "```Reply to any media file.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await eod(event, "reply to media file")
        return
    input_str = event.pattern_match.group(1)
    if input_str is None:
        await eod(event, f"Try `{hl}nfc voice` or`{hl}nfc mp3`")
        return
    if input_str in ["mp3", "voice"]:
        event = await eor(event, "converting...")
    else:
        await eod(event, f"Try `{hl}nfc voice` or`{hl}nfc mp3`")
        return
    try:
        start = datetime.datetime.now()
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            ),
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        end = datetime.datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if input_str == "voice":
            new_required_file_caption = "voice_" + str(round(time.time())) + ".opus"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "mp3_" + str(round(time.time())) + ".mp3"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("not supported")
            os.remove(downloaded_file_name)
            return
        logger.info(command_to_run)
        # TODO: re-write create_subprocess_exec 😉
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            force_document = False
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                ),
            )
            os.remove(new_required_file_name)
            await event.delete()


CmdHelp("convert").add_command(
    "stoi", "<reply to a sticker", "Converts the replied sticker into an image"
).add_command(
    "itos", "<reply to a image>", "Converts the replied image to sticker"
).add_command(
    "ftoi", "<reply to a image file", "Converts the replied file image to normal image"
).add_command(
    "gif",
    "<reply to a animated sticker",
    "Converts the replied animated sticker into gif",
).add_command(
    "ttf",
    "<reply to text>",
    "Converts the given text message to required file(given file name)",
).add_command(
    "nfc voice",
    "<reply to media to extract voice>",
    "Converts the replied media file to voice",
).add_command(
    "nfc mp3",
    "<reply to media to extract mp3>",
    "Converts the replied media file to mp3",
).add_info(
    "Converter."
).add_warning(
    "✅ Harmless Module."
).add()
