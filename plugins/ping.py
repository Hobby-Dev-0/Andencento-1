import datetime

from . import *


@Andencento.on(andencento_cmd(pattern="ping$"))
@Andencento.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def pong(user):
    if user.fwd_from:
        return
    start = datetime.datetime.now()
    event = await eor(user, "`·.·★ 🅟🅘🅝🅖 ★·.·´")
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(
        f"︻┳═一 🅟🅘🅝🅖 ︻┳═一\n\n    ⚘  `{ms}`\n    ⚘  __**🅞🅦🅝🅔🅡**__ **:**  {user_mention}"
    )


CmdHelp("ping").add_command(
    "ping", None, "Checks the ping speed of your ᴀɴᴅᴇɴᴄᴇɴᴛᴏ"
).add_warning("✅ Harmless Module").add()

# userbot
