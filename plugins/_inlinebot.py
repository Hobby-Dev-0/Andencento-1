import io
import re
from math import ceil

from config import Config
from telethon import custom, events
from userbot import CMD_LIST

from . import *

Andencento_pic = (
    Config.PMPERMIT_PIC or "https://telegra.ph/file/ac32724650ef92663fbd1.png"
)
cstm_pmp = Config.CUSTOM_PMPERMIT
ALV_PIC = Config.ALIVE_PIC
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
)

USER_BOT_WARN_ZERO = (
    "Enough Of Your Flooding In My Master's PM!! \n\n**š« Blocked and Reported**"
)
ANDENCENTO_FIRST = (
    "**š„ Andencento ULTRA Private Security š„**\n\nThis is to inform you that "
    "{} is currently unavailable.\nThis is an automated message.\n\n"
    "{}\n\n**Please Choose Why You Are Here!!**".format(Andencento_mention, mssge)
)
cmd = "commands"
andencento = Config.YOUR_NAME
if Config.BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        paginate_help(0, CMD_LIST, "helpme")
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id == bot.uid and query.startswith("Userbot"):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_LIST, "helpme")

            result = builder.article(
                "Ā© Andencento-UserBot Help",
                text=f"Andencento[š¤](https://telegra.ph/file/ac32724650ef92663fbd1.png)\nš° **{andencento}**\n\nš __No.of Plugins__ : `{len(CMD_LIST)}` \nšļø __Commands__ : `{len(apn)}`",
                buttons=buttons,
                link_preview=False,
            )
        elif event.query.user_id == bot.uid and query == "pm_warn":
            hel_l = ANDENCENTO_FIRST.format(Andencento_mention, mssge)
            result = builder.photo(
                file=Andencento_pic,
                text=hel_l,
                buttons=[
                    [
                        custom.Button.inline("š Request š", data="req"),
                        custom.Button.inline("š¬ Chat š¬", data="chat"),
                    ],
                    [custom.Button.inline("š« Spam š«", data="heheboi")],
                    [custom.Button.inline("Curious ā", data="pmclick")],
                ],
            )

        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**ā” ÉÉ¢ÉÕ¼ÉĪ±ŹŹ į“Ņ Andencento Userbot ā”**",
                buttons=[
                    [Button.url("š Repo š", "https://t.me/AndencentoSupport")],
                    [
                        Button.url(
                            "š Deploy š",
                            "https://heroku.com/deploy?template=https://github.com/Andencento/Deploy-Andencento",
                        )
                    ],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[āāā ā]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@TheEiva",
                text="""**Hey! This is [Andencento](https://t.me/Andencento) \nYou can know more about me from the links given below š**""",
                buttons=[
                    [
                        custom.Button.url("š„ CHANNEL š„", "https://t.me/Andencento"),
                        custom.Button.url(
                            "ā” GROUP ā”", "https://t.me/AndencentoSupport"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "āØ REPO āØ", "https://github.com/Andencento/Andencento"
                        ),
                        custom.Button.url(
                            "š° TUTORIAL š°",
                            "https://www.youtube.com/watch?v=9WxN6aq5wsQ",
                        ),
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"pmclick\\((.+?)\\)")
        )
    )
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for Other Users..."
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"š° This is Andencento PM Security for {Eiva_mention} to keep away unwanted retards from spamming PM..."
            )

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"reg\\((.+?)\\)")
        )
    )
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"ā **Request Registered** \n\n{Eiva_mention} will now decide to look for your request or not.\nš Till then wait patiently and don't spam else block!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**š Hey {Eiva_mention} !!** \n\nāļø You Got A Request From [{first_name}](tg://user?id={ok}) In PM!!"
            await bot.send_message(LOG_GP, tosend)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"chat\\((.+?)\\)")
        )
    )
    async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Ahh!! You here to do chit-chat!!\n\nPlease wait for {Eiva_mention} to come. Till then keep patience and don't spam."
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**š Hey {Eiva_mention} !!** \n\nāļø You Got A PM from  [{first_name}](tg://user?id={ok})  for random chats!!"
            await bot.send_message(LOG_GP, tosend)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"heheboi\\((.+?)\\)")
        )
    )
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(f"š„“ **Go away from here\nYou Are Blocked Now**")
            await bot(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await bot.send_message(
                LOG_GP,
                f"**Blocked**  [{first_name}](tg://user?id={ok}) \n\nReason:- Spam",
            )

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_next\\((.+?)\\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if (
            event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS
        ):  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(current_page_number + 1, CMD_LIST, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = (
                "Check Pinned Message in\n@ANDENCENTO And\nGet Your Own Userbot"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_prev\\((.+?)\\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if (
            event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS
        ):  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1, CMD_LIST, "helpme"  # pylint:disable=E0602
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = (
                "Check Pinned Message in\n@ANDENCENTO And\nGet Your Own Userbot"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"us_plugin_(.*)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            plugin_name = event.data_match.group(1).decode("UTF-8")
            help_string = ""
            try:
                for i in CMD_LIST[plugin_name]:
                    help_string += i
                    help_string += "\n"
            except BaseException:
                pass
            if help_string is "":
                reply_pop_up_alert = "{} is useless".format(plugin_name)
            else:
                reply_pop_up_alert = help_string
                reply_pop_up_alert += "\n Use .unload {} to remove this plugin\n\
          Ā© ANDENCENTo".format(
                    plugin_name
                )
            try:
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            except BaseException:
                with io.BytesIO(str.encode(reply_pop_up_alert)) as out_file:
                    out_file.name = "{}.txt".format(plugin_name)
                    await event.client.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption=plugin_name,
                    )
        else:
            reply_pop_up_alert = (
                "Check Pinned Message in\n@ANDENCENTO And\nGet Your Own Userbot"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = 8
    number_of_cols = 3
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline("{} {}".format(" ", x), data="us_plugin_{}".format(x))
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "Ā«Ā« Previous", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "Next Ā»Ā»", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs
