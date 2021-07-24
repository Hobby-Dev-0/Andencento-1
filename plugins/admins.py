from asyncio import sleep

from telethon.errors import (BadRequestError, ImageProcessFailedError,
                             PhotoCropSizeSmallError)
from telethon.errors.rpcerrorlist import (UserAdminInvalidError,
                                          UserIdInvalidError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto)

from sql.mute_sql import is_muted, mute, unmute

from . import *

lg_id = Config.LOGGER_ID
PP_TOO_SMOL = "🥴 The image is too small. Just like your crush's feelings"
PP_ERROR = (
    "😕 Failure while processing the image. Just like your proposal to your crush."
)
NO_ADMIN = "😪 I am not an admin here! Chutiya sala"
NO_PERM = "😐 Lack of Permissions. Just like your crush's feelings for you."
CHAT_PP_CHANGED = "😉 Chat Picture Changed Successfully"
INVALID_MEDIA = "🥴 Invalid media Extension. This is insane bruh. Grow some brain."


BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


@Andencento.on(andencento_cmd(pattern="setgpic$"))
@Andencento.on(sudo_cmd(pattern="setgpic$", allow_sudo=True))
@errors_handler
async def set_group_photo(gpic):
    if gpic.fwd_from:
        return
    if not gpic.is_group:
        await eor(gpic, "`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None
    if not admin and not creator:
        await eor(gpic, NO_ADMIN)
        return
    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await eor(gpic, INVALID_MEDIA)
    kraken = None
    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await eor(gpic, CHAT_PP_CHANGED)
            kraken = True
        except PhotoCropSizeSmallError:
            await eor(gpic, PP_TOO_SMOL)
        except ImageProcessFailedError:
            await eor(gpic, PP_ERROR)
        except Exception as e:
            await eor(gpic, f"**Error : **`{str(e)}`")
        if kraken:
            await gpic.client.send_message(
                lg_id,
                "#GROUPPIC\n"
                f"\nGroup profile pic changed "
                f"CHAT: {gpic.chat.title}(`{gpic.chat_id}`)",
            )


@Andencento.on(andencento_cmd(pattern="promote(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="promote(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def promote(promt):
    if promt.fwd_from:
        return
    chat = await promt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(promt, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    userevent = await eor(promt, "`Promoting User...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "ǟɖʍɨռ"
    if not user:
        return
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await userevent.edit(
            f"**🔥 Promoted  [{user.first_name}](tg://user?id={user.id})  Successfully In**  `{promt.chat.title}`!! \n**Admin Tag :**  `{rank}`"
        )
    except BadRequestError:
        await userevent.edit(NO_PERM)
        return
    await promt.client.send_message(
        lg_id,
        "#PROMOTE\n"
        f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
    )


@Andencento.on(andencento_cmd(pattern="demote(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="demote(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def demote(dmod):
    if dmod.fwd_from:
        return
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(dmod, NO_ADMIN)
        return
    userevent = await eor(dmod, "`Demoting User...`")
    rank = "ǟɖʍɨռ"
    user = await get_user_from_event(dmod)
    user = user[0]
    if not user:
        return
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await userevent.edit(NO_PERM)
        return
    await userevent.edit(
        f"**😪 Demoted  [{user.first_name}](tg://user?id={user.id})  Successfully In**  `{dmod.chat.title}`"
    )
    await dmod.client.send_message(
        lg_id,
        "#DEMOTE\n"
        f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)",
    )


@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@Andencento.on(andencento_cmd(pattern=r"mute ?(.*)"))
@Andencento.on(sudo_cmd(pattern=r"mute ?(.*)", allow_sudo=True))
async def muth(user):
    if user.is_private:
        await eor(user, "**Enough of your bullshit  !!**")
        await sleep(2)
        await user.get_reply_message()
        await user.client(GetFullUserRequest(user.chat_id))
        if is_muted(user.chat_id, user.chat_id):
            return await user.edit("Nigga is already muted here 🥴")
        if user.chat_id == ForGo10God:
            return await eod(user, "Nashe me hai kya lawde 🥴")
        try:
            mute(user.chat_id, user.chat_id)
        except Exception as e:
            await eor(user, f"**Error **\n`{str(e)}`")
        else:
            await eor(user, "**Chup Reh Lawde 🥴\n`**｀-´)⊃━☆ﾟ.*･｡ﾟ **`")
    else:
        userevent = await eor(user, "`Muting...`")
        input_str = user.pattern_match.group(1)
        chat = await user.get_chat()
        if user.reply_to_msg_id:
            userid = (await user.get_reply_message()).sender_id
            name = (await user.client.get_entity(userid)).first_name
        elif input_str:
            if input_str.isdigit():
                try:
                    userid = input_str
                    name = (await user.client.get_entity(userid)).first_name
                except ValueError as ve:
                    return await userevent.edit(str(ve))
            else:
                userid = (await user.client.get_entity(input_str)).id
                name = (await user.client.get_entity(userid)).first_name
        else:
            return await eod(userevent, "I Need a user to mute!!", 5)
        if userid == ForGo10God:
            return await eod(userevent, "Nashe me hai kya lawde", 5)
        if str(userid) in DEVLIST:
            return await eod(userevent, "**Error Muting God**", 7)
        try:
            await user.client.edit_permissions(
                chat.id,
                userid,
                until_date=None,
                send_messages=False,
            )
            await eor(
                userevent,
                f"**Successfully Muted**  [{name}](tg://user?id={userid}) **in**  `{chat.title}`",
            )
        except BaseException as be:
            await eor(userevent, f"`{str(be)}`")
        await user.client.send_message(
            lg_id,
            "#MUTE\n"
            f"\nUSER:  [{name}](tg://user?id={userid})\n"
            f"CHAT:  {chat.title}",
        )


@Andencento.on(andencento_cmd(pattern=r"unmute ?(.*)"))
@Andencento.on(sudo_cmd(pattern=r"unmute ?(.*)", allow_sudo=True))
async def nomuth(evn):
    if evn.is_private:
        await eor(evn, "Talk bich..")
        await sleep(1)
        await evn.client(GetFullUserRequest(evn.chat_id))
        if not is_muted(evn.chat_id, evn.chat_id):
            return await eor(evn, "Not even muted !!")
        try:
            unmute(evn.chat_id, evn.chat_id)
        except Exception as e:
            await eor(evn, f"**Error **\n`{str(e)}`")
        else:
            await eor(evn, "Abb boll bsdk.")
    else:
        userevent = await eor(evn, "`Unmuting...`")
        input_str = evn.pattern_match.group(1)
        chat = await evn.get_chat()
        if evn.reply_to_msg_id:
            userid = (await evn.get_reply_message()).sender_id
            name = (await evn.client.get_entity(userid)).first_name
        elif input_str:
            if input_str.isdigit():
                try:
                    userid = input_str
                    name = (await evn.client.get_entity(userid)).first_name
                except ValueError as ve:
                    return await userevent.edit(str(ve))
            else:
                userid = (await evn.client.get_entity(input_str)).id
                name = (await evn.client.get_entity(userid)).first_name
        else:
            return await eod(userevent, "I need a user to unmute!!", 3)
        try:
            await evn.client.edit_permissions(
                chat.id,
                userid,
                until_date=None,
                send_messages=True,
            )
            await eor(
                userevent,
                f"**Successfully Unmuted**  [{name}](tg://user?id={userid}) **in**  `{chat.title}`",
            )
        except BaseException as be:
            await eor(userevent, f"`{str(be)}`")
        await evn.client.send_message(
            lg_id,
            "#UNMUTE\n"
            f"\nUSER:  [{name}](tg://user?id={userid})\n"
            f"CHAT:  {chat.title}",
        )


@Andencento.on(andencento_cmd(pattern="ban(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="ban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def ban(bon):
    if bon.fwd_from:
        return
    userevent = await eor(bon, "`Banning Nigga...`")
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(bon, NO_ADMIN)
        return
    user, reason = await get_user_from_event(bon)
    if not user:
        return await userevent.edit("`Reply to a user or give username!!`")
    if str(user.id) in DEVLIST:
        return await userevent.edit("**Say again? Ban my creator??**")
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await userevent.edit(NO_PERM)
        return
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await userevent.edit(
            f"**Banned  [{user.first_name}](tg://user?id={user.id})  in** `[{bon.chat.title}]` !!\n\nMessage Nuking : **False**"
        )
        return
    if reason:
        await userevent.edit(
            f"**Bitch** [{user.first_name}](tg://user?id={user.id}) **is now banned in**  `[{bon.chat.title}]` !!\n**Reason :** `{reason}`"
        )
    else:
        await userevent.edit(
            f"**Bitch** [{user.first_name}](tg://user?id={user.id}) **is now banned in**  `[{bon.chat.title}]`!!"
        )
    await bon.client.send_message(
        lg_id,
        "#BAN\n"
        f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {bon.chat.title}(`{bon.chat_id}`)",
    )


@Andencento.on(andencento_cmd(pattern="unban(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="unban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def nothanos(unbon):
    if unbon.fwd_from:
        return
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(unbon, NO_ADMIN)
        return
    userevent = await eor(unbon, "`Unbanning...`")
    user = await get_user_from_event(unbon)
    user = user[0]
    if not user:
        return
    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await userevent.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Is Now Unbanned in**  `{unbon.chat.title}` !!"
        )
        await unbon.client.send_message(
            lg_id,
            "#UNBAN\n"
            f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)",
        )
    except UserIdInvalidError:
        await userevent.edit("Invalid UserId!! Please Recheck it!!")


@Andencento.on(andencento_cmd(pattern="pin($| (.*))"))
@Andencento.on(sudo_cmd(pattern="pin($| (.*))", allow_sudo=True))
@errors_handler
async def pin(msg):
    if msg.fwd_from:
        return
    chat = await msg.get_chat()
    ms_l = await bot.get_entity(msg.chat_id)
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(msg, NO_ADMIN)
        return
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        await eor(msg, "🥴 Reply to a message to pin it.")
        return
    options = msg.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await eor(msg, NO_PERM)
        return
    hmm = await eor(
        msg,
        f"📌 **Pinned  [this message](https://t.me/c/{ms_l.id}/{to_pin})  Successfully!**",
    )
    user = await get_user_from_id(msg.sender_id, msg)
    await msg.client.send_message(
        lg_id,
        "#PIN\n"
        f"\nADMIN: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
        f"LOUD: {not is_silent}",
    )
    await sleep(3)
    try:
        await hmm.delete()
    except:
        pass


@Andencento.on(andencento_cmd(pattern="kick(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="kick(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def kick(usr):
    if usr.fwd_from:
        return
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(usr, NO_ADMIN)
        return
    user, reason = await get_user_from_event(usr)
    if not user:
        return await eor(usr, "`Couldn't fetch user info...`")
    if str(user.id) in DEVLIST:
        return await eor(usr, "**Turn back, Go straight and fuck off!!**")
    userevent = await eor(usr, "`Kicking...`")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await userevent.edit(NO_PERM + f"\n`{str(e)}`")
        return
    if reason:
        await userevent.edit(
            f"**🏃 Kicked**  [{user.first_name}](tg://user?id={user.id})'s **Butt from** `{usr.chat.title}!`\nReason: `{reason}`"
        )
    else:
        await userevent.edit(
            f"**🏃 Kicked**  [{user.first_name}](tg://user?id={user.id})'s **Butt from** `{usr.chat.title}!`"
        )
    await usr.client.send_message(
        lg_id,
        "#KICK\n"
        f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n",
    )


@Andencento.on(andencento_cmd(pattern=f"zombies ?(.*)"))
@Andencento.on(sudo_cmd(pattern=f"zombies ?(.*)", allow_sudo=True))
async def rm_deletedacc(show):
    if show.fwd_from:
        return
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`No zombies or deleted accounts found in this group, Group is clean`"
    if con != "clean":
        event = await eor(show, "**Searching For Zombies...**")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**🆘 ALERT !!**\n\n`{del_u}`  **Zombies detected ☣️\nClean them by using**  `{hl}zombies clean`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eod(show, NO_ADMIN)
        return
    event = await eor(show, "🧹 Purging out zombies from this group...")
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_or_reply(event, "`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**Ongoing Zombie Purge!!**\n\n**Zombies Killed :**  `{del_u}`"
    if del_a > 0:
        del_status = (
            f"**Zombies Killed**  `{del_u}`\n\n`{del_a}`  **Zombies Holds Immunity!!**"
        )
    await edit_or_reply(event, del_status)
    await show.client.send_message(
        lg_id,
        f"#ZOMBIES\
        \n{del_status}\
       \nCHAT: {show.chat.title}(`{show.chat_id}`)",
    )


@Andencento.on(andencento_cmd(pattern="undlt$"))
@Andencento.on(sudo_cmd(pattern="undlt$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await event.client.get_admin_log(
            event.chat_id, limit=5, edit=False, delete=True
        )
        deleted_msg = "Deleted message in this group:"
        for i in a:
            deleted_msg += "\n👉`{}`".format(i.old.message)
        await eor(event, deleted_msg)
    else:
        await eor(
            event, "`You need administrative permissions in order to do this command`"
        )
        await sleep(3)
        try:
            await event.delete()
        except:
            pass


async def get_user_from_event(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await event.edit("Could not fetch info of that user.")
            return None
    return user_obj, extra


async def get_user_from_id(user, event):
    if event.fwd_from:
        return
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


CmdHelp("admins").add_command(
    "setgpic", "<reply to image>", "Changes the groups display picture"
).add_command(
    "promote",
    "<username/reply> <custom rank (optional)>",
    "Provides admins right to a person in the chat.",
).add_command(
    "demote", "<username/reply>", "Revokes the person admin permissions in the chat."
).add_command(
    "ban", "<username/reply> <reason (optional)>", "Bans the person off your chat."
).add_command(
    "unban", "<username/reply>", "Removes the ban from the person in the chat."
).add_command(
    "mute",
    "<reply>/<userid or username>",
    "Mutes the person in the group. Works on non-admins only",
).add_command(
    "unmute", "<reply>/<userid or username>", "Unmutes the person muted in that group."
).add_command(
    "pin", "<reply> or .pin loud", "Pins the replied message in Group"
).add_command(
    "kick", "<username/reply>", "kick the person off your chat"
).add_command(
    "zombies", None, "Check If The Group is Infected By Zombies."
).add_command(
    "zombies clean", None, "Clears all the zombies in the group."
).add_command(
    "iundlt", None, "display last 5 deleted messages in group."
).add_info(
    "Admins Things!"
).add_warning(
    "✅ Harmless Module."
).add()
