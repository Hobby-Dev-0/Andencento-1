import asyncio

from telethon import events
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from sql import gmute_sql as gsql
from sql.gban_sql import all_gbanned, gbaner, is_gbanned, ungbaner

from . import *


@Andencento.on(sudo_cmd(pattern=r"gban ?(.*)", allow_sudo=True))
async def _(event):
    await eor(event, "`Sudo Restricted Command Sur`")
    return


@Andencento.on(sudo_cmd(allow_sudo=True, pattern=r"ungmute ?(\d+)?"))
async def _(event):
    await eor(event, "`Sudo Restricted Command Sur`")
    return


@Andencento.on(sudo_cmd(pattern="listgban$", allow_sudo=True))
async def _(event):
    await eor(event, "`Sudo Restricted Command Sur`")
    return


@Andencento.on(sudo_cmd(pattern=r"ungban ?(.*)", allow_sudo=True))
async def _(event):
    await eor(event, "`Sudo Restricted Command Sur`")
    return


@Andencento.on(sudo_cmd(pattern=r"gkick ?(.*)", allow_sudo=True))
async def _(event):
    await eor(event, "`Sudo Restricted Command Sur`")
    return


@Andencento.on(sudo_cmd(allow_sudo=True, pattern=r"gmute ?(\d+)?"))
async def _(event):
    await eor(event, "`Sudo Restricted Command Sur`")
    return


@Andencento.on(andencento_cmd(pattern=r"gban ?(.*)"))
async def _(event):
    user = await eor(event, "`Gbanning this retard`")
    reason = ""
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await eod(
            user, "**To gban a user i need a userid or reply to his/her message!!**"
        )
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == ForGo10God:
        return await eod(user, "🥴 **Nashe me hai kya lawde ‽**")
    if str(userid) in DEVLIST:
        return await eod(
            user,
            "😑 **Nashe me hai kya lawde. Apne bap ko gban dene chala h bhadwe baap se backchodi nahi ?¿ smjha‽**",
        )
    if is_gbanned(userid):
        return await eod(
            user,
            "This kid is already gbanned and added to my **Gban Watch!!**",
        )
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(
                    gfuck.id, userid, view_messages=False
                )
                chats += 1
            except BaseException:
                pass
    gbaner(userid)
    gmsg = f"🥴 [{name}](tg://user?id={userid}) **Is now GBanned by** {user_mention} **in**  `{chats}`  **Agli bar se backchodi nahi betichod**\n\n📍 Also Added to Gban Watch!!**!\n**🔰 Total Chats :**  `{chats}`"
    if reason != "":
        gmsg += f"\n**🔰 Reason :**  `{reason}`"
    ogmsg = f"[{name}](tg://user?id={userid}) **Is now GBanned by** {user_mention} **in**  `{chats}`  **Agli bar se backchodi nahi betichod**\n\n**📍 Also Added to Gban Watch!!**!\n**🔰 Total Chats :**  `{chats}`"
    if reason != "":
        ogmsg += f"\n**🔰 Reason :**  `{reason}`"
    if Config.ABUSE == "ON":
        await user.edit(ogmsg)
    else:
        await user.edit(ogmsg)


@Andencento.on(andencento_cmd(pattern=r"ungban ?(.*)"))
async def _(event):
    user = await eor(event, "`Ungban in progress...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(user, "`Reply to a user or give their userid... `")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if not is_gbanned(userid):
        return await eod(user, "`User is not gbanned.`")
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(
                    gfuck.id, userid, view_messages=True
                )
                chats += 1
            except BaseException:
                pass
    ungbaner(userid)
    await user.edit(
        f"📍 [{name}](tg://user?id={userid}) **is now Ungbanned from `{chats}` chats and removed from Gban Watch!! Agli bar se backchodi na karna**",
    )


@Andencento.on(andencento_cmd(pattern="listgban$"))
async def already(event):
    gbanned_users = all_gbanned()
    GBANNED_LIST = "**Gbanned Users :**\n"
    if len(gbanned_users) > 0:
        for user in gbanned_users:
            name = (await bot.get_entity(int(user))).first_name
            GBANNED_LIST += f"📍 [{name}](tg://user?id={user.chat_id})\n"
    else:
        GBANNED_LIST = "No Gbanned Users!!"
    await edit_or_reply(event, GBANNED_LIST)


@Andencento.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        if is_gbanned(str(user.id)):
            if chat.admin_rights:
                try:
                    await event.client.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Retard Id :**  [{user.first_name}](tg://user?id={user.id})\n"
                    gban_watcher += (
                        f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    )
                    await event.reply(gban_watcher)
                except BaseException:
                    pass


@Andencento.on(andencento_cmd(pattern=r"gkick ?(.*)"))
async def gkick(event):
    user = await eor(event, "`Kicking globally...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(user, "`Reply to some msg or add their id.`")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == ForGo10God:
        return await eod(user, "**🥴 Nashe me hai kya lawde!!**")
    if str(userid) in DEVLIST:
        return await eod(user, "**😪 I'm not going to gkick my developer!!**")
    async for gkick in event.client.iter_dialogs():
        if gkick.is_group or gkick.is_channel:
            try:
                await bot.kick_participant(gkick.id, userid)
                chats += 1
            except BaseException:
                pass
    gkmsg = f"🏃 **Globally Kicked** [{name}](tg://user?id={userid})'s butts !! \n\n📝 **Chats :**  `{chats}`"
    if Config.ABUSE == "ON":
        await user.edit(gkmsg)
    else:
        await user.edit(gkmsg)


@Andencento.on(andencento_cmd(pattern=r"gmute ?(\d+)?"))
async def gm(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await eor(event, "`Trying to gmute user...`")
        await asyncio.sleep(2)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(
            event, "Need a user to gmute. Reply or give userid to gmute them.."
        )
    event.chat_id
    await event.get_chat()
    if gsql.is_gmuted(userid, "gmute"):
        return await eod(event, "This kid is already Gmuted.")
    try:
        if str(userid) in DEVLIST:
            return await eod(event, "**Sorry I'm not going to gmute them..**")
    except:
        pass
    try:
        gsql.gmute(userid, "gmute")
    except Exception as e:
        await eod(event, "Error occured!\nError is " + str(e))
    else:
        await eor(event, "Shhh.... Now keep quiet !!")


@Andencento.on(andencento_cmd(outgoing=True, pattern=r"ungmute ?(\d+)?"))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await eor(event, "`Trying to ungmute !!`")
        await asyncio.sleep(2)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(
            event,
            "Please reply to a user or add their into the command to ungmute them.",
        )
    event.chat_id
    if not gsql.is_gmuted(userid, "gmute"):
        return await eod(event, "I don't remember I gmuted him...")
    try:
        gsql.ungmute(userid, "gmute")
    except Exception as e:
        await eod(event, "Error occured!\nError is " + str(e))
    else:
        await eor(event, "Ok!! Speak")


marculs = 9
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, MessageEntityMentionName

from . import *


async def get_full_user(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Itz not possible without an user ID`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit(
                "Error... Please report at @AndencentoSupport", str(err)
            )
    return user_obj, extra


global hawk, moth
hawk = "admin"
moth = "owner"


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


@Andencento.on(andencento_cmd(pattern="gpromote ?(.*)"))
async def gben(userbot):
    dc = dark = userbot
    i = 0
    await dc.get_sender()
    me = await userbot.client.get_me()
    await dark.edit("`promoting...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    if userbot.is_private:
        user = userbot.chat
        rank = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, rank = await get_full_user(userbot)
    except:
        pass
    if me == user:
        await dark.edit("U want to promote urself 😑😑 waao..")
        return
    try:
        if not rank:
            rank = "ㅤㅤ"
    except:
        return await dark.edit(f"**Something W3NT Wrong 🤔**")
    if user:
        telchanel = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        rgt = ChatAdminRights(
            add_admins=False,
            invite_users=True,
            change_info=False,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
        )
        for x in telchanel:
            try:
                await userbot.client(EditAdminRequest(x, user, rgt, rank))
                i += 1
                await dark.edit(f"**Promoted in Chats **: `{i}`")
            except:
                pass
    else:
        await dark.edit(f"**Reply to a user you dumbo !!**")
    return await dark.edit(
        f"**Globally promoted [{user.first_name}](tg://user?id={user.id})\n On Chats😏 : {i} **"
    )


@Andencento.on(andencento_cmd(pattern="gdemote ?(.*)"))
async def gben(userbot):
    dc = dark = userbot
    i = 0
    await dc.get_sender()
    me = await userbot.client.get_me()
    await dark.edit("`demoting...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    if userbot.is_private:
        user = userbot.chat
        rank = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, rank = await get_full_user(userbot)
    except:
        pass
    if me == user:
        await dark.edit("U want to demote urself 😑😑 waao..")
        return
    try:
        if not rank:
            rank = "ㅤㅤ"
    except:
        return await dark.edit(f"**Something W3NT Wrong 🤔**")
    if user:
        telchanel = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        rgt = ChatAdminRights(
            add_admins=None,
            invite_users=None,
            change_info=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None,
        )
        for x in telchanel:
            try:
                await userbot.client(EditAdminRequest(x, user, rgt, rank))
                i += 1
                await dark.edit(f"**Demoted in Chats **: `{i}`")
            except:
                pass
    else:
        await dark.edit(f"**Reply to a user you dumbo !!**")
    return await dark.edit(
        f"**Globally Demoted [{user.first_name}](tg://user?id={user.id})\n On Chats😏 : {i} **"
    )


@command(incoming=True)
async def watcher(event):
    if gsql.is_gmuted(event.sender_id, "gmute"):
        await event.delete()


CmdHelp("global").add_command(
    "gban",
    "<reply>/<userid>",
    "Globally Bans the mentioned user in 'X' chats you are admin with ban permission.",
).add_command(
    "ungban", "<reply>/<userid>", "Globally Unbans the user in 'X' chats you are admin!"
).add_command(
    "listgban", None, "Gives the list of all GBanned Users."
).add_command(
    "gkick", "<reply>/<userid>", "Globally Kicks the user in 'X' chats you are admin!"
).add_command(
    "gmute", "<reply> or <userid>", "Globally Mutes the User."
).add_command(
    "ungmute", "<reply> or <userid>", "Globally Unmutes the gmutes user."
).add_command(
    "gpromote", "<reply> or <userid>", "Globally promotes the User."
).add_command(
    "ungdemote", "<reply> or <userid>", "Globally demotes the gpromoted user."
).add_info(
    "Global Admin Tool."
).add_warning(
    "✅ Harmlesss Module."
).add()
