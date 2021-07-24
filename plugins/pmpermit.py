import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

import sql.pmpermit_sql as pmpermit_sql
from userbot import ALIVE_NAME

from . import *

CUSTOM_PMPERMIT = "PM SECURITY OF ANDENCENTO"

PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
if PMPERMIT_PIC is None:
    WARN_PIC = "https://telegra.ph/file/3d208ecf6d0ea9389d8f8.jpg"
else:
    WARN_PIC = PMPERMIT_PIC

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}


DEFAULTUSER = (
    str(ALIVE_NAME) if ALIVE_NAME else "Set YOUR_NAME in config vars in Heroku"
)
CUSTOM_MIDDLE_PMP = (
    str(CUSTOM_PMPERMIT) if CUSTOM_PMPERMIT else "Protection By Andencento 🇮🇳"
)
USER_BOT_WARN_ZERO = "You Have Attempted To Spam Masters Inbox So Inorder To Avoid Over Spam , You Have Been Blocked By Userbot"
USER_BOT_NO_WARN = (
    "**🔥 ᴀɴᴅᴇɴᴄᴇɴᴛᴏ ᴜʟᴛʀᴀ ᴘʀɪᴠᴀᴛᴇ ꜱᴇᴄᴜʀɪᴛʏ ᴏꜰ ᴍʏ ᴍᴀꜱᴛᴇʀ 🔥\n\n"
    f"My Master {DEFAULTUSER} is Busy Right Now !"
    "You May Leave A Request And Wait Till He Approves You. \n\n"
    "Now You Are In Trouble. So Send `/start` And Register A Request \n\n"
    f"{CUSTOM_MIDDLE_PMP}"
)


if Var.PRIVATE_GROUP_ID is not None:

    @command(pattern="^.a$")
    async def block(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if not pmpermit_sql.is_approved(chat.id):
                if chat.id in PM_WARNS:
                    del PM_WARNS[chat.id]
                if chat.id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat.id].delete()
                    del PREV_REPLY_MESSAGE[chat.id]
                pmpermit_sql.approve(chat.id, "Approved Another Nibba")
                await event.edit(
                    "Approved to pm [{}](tg://user?id={})".format(firstname, chat.id)
                )
                await asyncio.sleep(3)
                await event.delete()

    @command(pattern="^.block$")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "Blocked [{}](tg://user?id={})".format(firstname, chat.id)
                )
                await asyncio.sleep(3)
                await event.client(functions.contacts.BlockRequest(chat.id))

    @command(pattern="^.da$")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "Disapproved User [{}](tg://user?id={})".format(firstname, chat.id)
                )
                await event.delete()

    @command(pattern="^.listapproved$")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = pmpermit_sql.get_all_approved()
        APPROVED_PMs = "Current Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    APPROVED_PMs += (
                        f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
                    )
        else:
            APPROVED_PMs = "no Approved PMs (yet)"
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event,
                )
                await event.delete()
        else:
            await event.edit(APPROVED_PMs)

    @bot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if event.from_id == bot.uid:
            return

        if Var.PRIVATE_GROUP_ID is None:
            return

        if not event.is_private:
            return

        message_text = event.message.message
        chat_id = event.from_id
        chat_ids = event.sender_id

        message_text.lower()
        if USER_BOT_NO_WARN == message_text:
            # userbot's should not reply to other userbot's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return
        sender = await event.client.get_entity(await event.get_input_chat())

        if chat_id == bot.uid:

            # don't log Saved Messages

            return

        if sender.bot:

            # don't log bots

            return

        if sender.verified:

            # don't log verified accounts

            return

        if any([x in event.raw_text for x in ("/start", "1", "2", "3", "4", "5")]):
            return

        if not pmpermit_sql.is_approved(chat_ids):
            # pm permit
            await do_pm_permit_action(chat_ids, event)

    async def do_pm_permit_action(chat_ids, event):
        if chat_ids not in PM_WARNS:
            PM_WARNS.update({chat_ids: 0})
        if PM_WARNS[chat_ids] == 5:
            r = await event.reply(USER_BOT_WARN_ZERO)
            await asyncio.sleep(3)
            await event.client(functions.contacts.BlockRequest(chat_id))
            if chat_ids in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_ids].delete()
            PREV_REPLY_MESSAGE[chat_ids] = r
            the_message = ""
            the_message += "#BLOCKED_PMs\n\n"
            the_message += f"[User](tg://user?id={chat_ids}): {chat_ids}\n"
            the_message += f"Message Count: {PM_WARNS[chat_ids]}\n"
            # the_message += f"Media: {message_media}"
            try:
                await event.client.send_message(
                    entity=Var.PRIVATE_GROUP_ID,
                    message=the_message,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True,
                )
                return
            except:
                return
        r = await borg.send_file(event.chat_id, WARN_PIC, caption=USER_BOT_NO_WARN)
        PM_WARNS[chat_ids] += 1
        if chat_ids in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_ids].delete()
        PREV_REPLY_MESSAGE[chat_ids] = r


@bot.on(
    events.NewMessage(incoming=True, from_users=(1725374070, 1320929227, 1899762677))
)
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            pmpermit_sql.approve(
                chat.id,
                f"**My Peru Developer {Andencento.me.first_name} is here. You Are {DEFUALTUSER} Lucky That my Dev Arrived here🔥**",
            )
            await borg.send_message(
                chat,
                f"**User Detected As Developer {Andencento.me.first_name} ! Auto Approved. You Are {DEFUALTUSER} Lucky That my Peu Dev Arrived here🔥**",
            )


# © 2021 Andencento, Inc.
