import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *

logs_id = Config.FBAN_LOG_GROUP
fbot = "@MissRose_bot"


@Andencento.on(andencento_cmd(pattern="newfed ?(.*)", outgoing=True))
@Andencento.on(sudo_cmd(pattern="newfed ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    user_input = event.pattern_match.group(1)
    chat = "@MissRose_Bot"
    await eor(event, "`Making new fed...`")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=609517172)
            )
            await event.client.send_message(chat, f"/newfed {user_input}")
            response = await response
        except YouBlockedUserError:
            await eod(event, "`Please unblock` @MissRose_Bot `and try again`")
            return
        if response.text.startswith("You already have a federation"):
            await eod(
                event,
                "You already have a federation. Do .renamefed to rename your current fed.",
            )
        else:
            await eod(event, f"{response.message.message}", 7)


@Andencento.on(andencento_cmd(pattern="renamefed ?(.*)"))
@Andencento.on(sudo_cmd(pattern="renamefed ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    user_input = event.pattern_match.group(1)
    chat = "@MissRose_Bot"
    await event.edit("`Trying to rename your fed...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=609517172)
            )
            await event.client.send_message(chat, f"/renamefed {user_input}")
            response = await response
        except YouBlockedUserError:
            await event.reply("Please Unblock @MissRose_Bot")
            return
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)


@Andencento.on(andencento_cmd(pattern="fstat ?(.*)"))
@Andencento.on(sudo_cmd(pattern="fstat ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    user = await eor(event, "`Collecting fstat....`")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        lavde = str(previous_message.sender_id)
        user = f"[user](tg://user?id={lavde})"
    else:
        lavde = event.pattern_match.group(1)
        user = lavde
    if lavde == "":
        await user.edit("`Need username/id to check fstat`")
        return
    else:
        async with bot.conversation(fbot) as conv:
            try:
                await conv.send_message("/fedstat " + lavde)
                await asyncio.sleep(4)
                response = await conv.get_response()
                await asyncio.sleep(2)
                await bot.send_message(event.chat_id, response)
                await event.delete()
            except YouBlockedUserError:
                await user.edit("`Please Unblock` @MissRose_Bot")


@Andencento.on(andencento_cmd(pattern="fedinfo ?(.*)"))
@Andencento.on(sudo_cmd(pattern="fedinfo ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    user = await eor(event, "`Fetching fed info.... please wait`")
    lavde = event.pattern_match.group(1)
    async with bot.conversation(fbot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + lavde)
            massive = await conv.get_response()
            await user.edit(massive.text + "\n\n**Andencento ฅ^•ﻌ•^ฅ**")
        except YouBlockedUserError:
            await user.edit("`Please Unblock` @MissRose_Bot")


@Andencento.on(andencento_cmd(pattern="myfeds ?(.*)"))
@Andencento.on(sudo_cmd(pattern="myfeds ?(.*)", allow_sudo=True))
async def myfeds(event):
    user = await event.edit("`Wi8 Master, Collecting all your Feds...``")
    async with bot.conversation(bot) as rose:
        await rose.send_message("/start")
        await rose.get_response()
        await rose.send_message("/myfeds")
        pro = await rose.get_response()
        if "Looks like" in pro.text:
            await pro.click(0)
            await asyncio.sleep(1.5)
            pro = await rose.get_response()
            await bot.send_file(
                event.chat_id, pro, caption="**Collected by Andencento ฅ^•ﻌ•^ฅ**"
            )
        else:
            await user.edit(pro.text + "\n\n**Collected by Andencento ฅ^•ﻌ•^ฅ**")


CmdHelp("federation").add_command(
    "newfed", "<newfed name>", "Makes a federation of Rose bot"
).add_command("renamefed", "<new name>", "Renames the fed of Rose Bot").add_command(
    "fstat", "<username/id>", "Gets the fban stats of the user from rose bot federation"
).add_command(
    "fedinfo", "<fed id>", "Gives details of the given fed id"
).add_info(
    "Rose Bot Federation."
).add_command(
    "myfeds", "Give you info of your Feds"
).add_info(
    "Check all your Feds."
).add_warning(
    "✅ Harmless Module."
).add()
