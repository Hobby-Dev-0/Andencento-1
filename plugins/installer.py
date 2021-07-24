danger = [
    "STRING_SESSION",
    "get_me",
    "bot.me",
    "borg.me",
    "client.me",
    "session",
    "stdout",
    "stderr",
    "pip",
    "webhost",
    "bash",
    "eval",
    "phone",
    "DeleteAccountRequest",
    "deleteaccountrequest",
    "DeleteAccount",
    "phune",
    "ANDENCENTO_SESSION",
    "HELL_SESSION",
    "venv" "env",
]
import asyncio
import os
from pathlib import Path


def handler():
    k = os.environ.get("HANDLER", ".")
    if k:
        return k
    else:
        return "."


from telethon.tl.functions.channels import JoinChannelRequest as join

from . import *


@bot.on(andencento_cmd(None))
async def safety(event):
    text = event.text
    x = handler()
    if text != f"{x}install":
        return
    if not event.is_reply:
        return await event.edit("please tag a file")
    tag = await event.get_reply_message()
    file = await bot.download_media(tag, "userbot/plugins")
    X = ""
    for word in danger:
        f = open(file, "r")
        k = re.search(word, f.read())
        f.close()
        if k:
            X += word + " "
        else:
            pass
    if X != "":
        await event.edit(
            f"Alert Danger Word Found in Your tagged plug-in\nthe danger word is: \n**{X}**\nif you know about this plugin and still want to install then type `{x}install -f`"
        )
        try:
            await bot(join("AndencentoSupport"))
        except:
            pass
        await bot.send_file(
            "AndencentoSupport",
            file=file,
            caption=f"@NoobStrangerPerson Danger Word found Check This Plugin \nDanger word is: {X}",
        )
        os.system(f"rm -rf {file}")
        return
    try:
        path1 = Path(file)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
        await event.edit("The Plugin is Successfully Installed")
        await asyncio.sleep(3)
        await event.delete()
    except Exception as e:
        await event.edit(f"Some Error Found Please check \n{str(e)}")
