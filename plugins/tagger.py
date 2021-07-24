from telethon import custom, events
from telethon.tl.types import Channel
from telethon.utils import get_display_name

from . import *

if Config.TAG_LOGGER:
    tagger = int(Config.TAG_LOGGER)

if Config.TAG_LOGGER:

    @Andencento.on(
        events.NewMessage(
            incoming=True,
            blacklist_chats=Config.BL_CHAT,
            func=lambda e: (e.mentioned),
        )
    )
    async def all_messages_catcher(event):
        await event.forward_to(tagger)
        ammoca_message = ""
        kraken = await event.client.get_entity(event.sender_id)
        if kraken.bot or kraken.verified or kraken.support:
            return
        krakenm = f"[{get_display_name(kraken)}](tg://user?id={kraken.id})"
        where_ = await event.client.get_entity(event.chat_id)
        where_m = get_display_name(where_)
        button_text = "See the tag 📬"
        if isinstance(where_, Channel):
            message_link = f"https://t.me/c/{where_.id}/{event.id}"
        else:
            message_link = f"tg://openmessage?chat_id={where_.id}&message_id={event.id}"
        ammoca_message += f"👆 #TAG\n\n{krakenm} `just tagged you...` \nWhere?\nIn [{where_m}]({message_link})\n__Tap to go the tagged msg__📬🚶"
        if tagger is not None:
            await bot.send_message(
                entity=tagger,
                message=ammoca_message,
                link_preview=False,
                buttons=[[custom.Button.url(button_text, message_link)]],
                silent=True,
            )
        else:
            return


@Andencento.on(andencento_cmd(pattern=r"tagall (.*)", outgoing=True))
@Andencento.on(sudo_cmd(pattern=r"tagall (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = event.pattern_match.group(1)
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, 100):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()
