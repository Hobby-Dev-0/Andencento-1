import io
import re
from math import ceil
from config import Config
from userbot import CMD_LIST, CMD_HELP
from telethon import custom, events
Andencento_pic = Config.PMPERMIT_PIC or "https://telegra.ph/file/ac32724650ef92663fbd1.png"
cstm_pmp = Config.CUSTOM_PMPERMIT
ALV_PIC = Config.ALIVE_PIC
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
)

USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**🚫 Blocked and Reported**"
ANDENCENTO_FIRST = (
    "**🔥 Andencento ULTRA Private Security 🔥**\n\nThis is to inform you that "
    "{} is currently unavailable.\nThis is an automated message.\n\n"
    "{}\n\n**Please Choose Why You Are Here!!**".format(Eiva_mention, mssge))
cmd = "commands"
andencento = Config.YOUR_NAME
if Config.BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        button = paginate_help(0, CMD_LIST, "helpme")
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id == bot.uid and query.startswith("Userbot"):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_LIST, "helpme")
            
            result = builder.article(
                "© Andencento-UserBot Help",
                text=f"🔰 **{andencento}**\n\n📜 __No.of Plugins__ : `{len(CMD_LIST)}` \n🗂️ __Commands__ : `{len(apn)}`",
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
                        custom.Button.inline("📝 Request 📝", data="req"),
                        custom.Button.inline("💬 Chat 💬", data="chat"),
                    ],
                    [custom.Button.inline("🚫 Spam 🚫", data="heheboi")],
                    [custom.Button.inline("Curious ❓", data="pmclick")],
                ],
            )

        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**⚡ ɛɢɛռɖαʀʏ ᴀғ Andencento Userbot ⚡**",
                buttons=[
                    [Button.url("📑 Repo 📑", "https://t.me/AndencentoSupport")],
                    [Button.url("🚀 Deploy 🚀", "https://heroku.com/deploy?template=https://github.com/Andencento/Deploy-Andencento")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[‏‏‎ ‎]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@TheEiva",
                text="""**Hey! This is [Andencento](https://t.me/Andencento) \nYou can know more about me from the links given below 👇**""",
                buttons=[
                    [
                        custom.Button.url("🔥 CHANNEL 🔥", "https://t.me/Andencento"),
                        custom.Button.url(
                            "⚡ GROUP ⚡", "https://t.me/AndencentoSupport"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "✨ REPO ✨", "https://github.com/Andencento/Andencento"),
                        custom.Button.url
                    (
                            "🔰 TUTORIAL 🔰", "https://www.youtube.com/watch?v=9WxN6aq5wsQ"
                    )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_next\((.+?)\)")
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
            data=re.compile(b"helpme_prev\((.+?)\)")
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
            except:
                pass
            if help_string is "":
                reply_pop_up_alert = "{} is useless".format(plugin_name)
            else:
                reply_pop_up_alert = help_string
                reply_pop_up_alert += "\n Use .unload {} to remove this plugin\n\
          © ANDENCENTo".format(
                    plugin_name
                )
            try:
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            except:
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
                    "«« Previous", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "Next »»", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs
