import asyncio
import os

from . import *


@Andencento.on(andencento_cmd(pattern=r"unpack", outgoing=True))
@Andencento.on(sudo_cmd(pattern=r"unpack"))
async def _(event):
    b = await event.client.download_media(await event.get_reply_message())
    a = open(b, "r")
    c = a.read()
    a.close()
    a = await eor(event, "**Unpacking...**")
    if len(c) > 4095:
        await a.edit(
            "Telegram Word Limit Of **4095** words exceeded. \n**ABORTING PROCESS !!**"
        )
    else:
        await event.client.send_message(event.chat_id, f"{c}")
        await a.delete()
    os.remove(b)


@Andencento.on(andencento_cmd(pattern=r"pack ?(.*)", outgoing=True))
@Andencento.on(sudo_cmd(pattern=r"pack ?(.*)", allow_sudo=True))
async def _(event):
    a = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    b = open(input_str, "w")
    b.write(str(a.message))
    b.close()
    a = await edit_or_reply(event, f"Packing into `{input_str}`")
    await asyncio.sleep(2)
    await a.edit(f"Uploading `{input_str}`")
    await asyncio.sleep(2)
    await event.client.send_file(event.chat_id, input_str)
    await a.delete()
    os.remove(input_str)


CmdHelp("packer").add_command(
    "unpack",
    "<reply to a file>",
    "Read contents of file and send as a telegram message.",
).add_command(
    "pack",
    "<reply to text> <filename . extension>",
    "Packs the text and sends as a file of given extension",
    "<reply to text> example.py",
).add_info(
    "Packer Iz Here !"
).add_warning(
    "✅ Harmless Module."
).add()
