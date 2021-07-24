import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@Andencento.on(andencento_cmd(pattern=r"(qbot|ss) ?(.*)", outgoing=True))
@Andencento.on(sudo_cmd(pattern=r"(qbot|ss) ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eod(event, "```Reply to any user's message.```")
        return
    reply_message = await event.get_reply_message()
    user = event.pattern_match.group(1)
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await eod(event, "```Reply to actual user's message.```")
        return
    await eor(event, "```Making a Quote...```")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            first = await conv.send_message(f"/qcolor {user}")
            ok = await conv.get_response()
            await asyncio.sleep(2)
            second = await bot.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("Please unblock @QuotLyBot and try again!!")
            return
        if response.text.startswith("Hi!"):
            await eor(event, "Can you kindly disable your forward privacy settings.")
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
    await bot.delete_messages(conv.chat_id, [first.id, ok.id, second.id, response.id])


CmdHelp("qbot").add_command(
    "ss or qbot",
    "<reply to msg> <bg colour>",
    "Makes the sticker of the replied text, sticker, pic.",
    "ss black <reply to a msg>",
).add_info("Makes Quoted Sticker.").add_warning("✅ Harmless Module.").add()
