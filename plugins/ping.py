import datetime

from . import *


@Andencento.on(andencento_cmd(pattern="ping$"))
@Andencento.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def pong(user):
    if user.fwd_from:
        return
    start = datetime.datetime.now()
    event = await eor(user, "`Β·.Β·β ππππ βΒ·.Β·Β΄")
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(
        f"οΈ»β³βδΈ ππππ οΈ»β³βδΈ\n\n    β  `{ms}`\n    β  __**ππ¦πππ‘**__ **:**  {user_mention}"
    )


CmdHelp("ping").add_command(
    "ping", None, "Checks the ping speed of your α΄Ι΄α΄α΄Ι΄α΄α΄Ι΄α΄α΄"
).add_warning("β Harmless Module").add()

# userbot
