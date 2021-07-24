from . import *

# Credits to @ForGo10God developer of Andencento .
# This is my first plugin that I made when I released first Andencento .
# Modified to work in groups with inline mode disabled.
# Added error msg if no voice is found.
# So please dont remove credit.
# You can use it in your repo. But dont remove these lines...


@Andencento.on(andencento_cmd(pattern="mev(?: |$)(.*)", outgoing=True))
@Andencento.on(sudo_cmd(pattern="mev(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    user = kraken.pattern_match.group(1)
    if not user:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            await edit_or_reply(
                kraken,
                "`Sir please give some query to search and download it for you..!`",
            )
            return

    troll = await bot.inline_query("TrollVoiceBot", f"{(deEmojify(user))}")
    if troll:
        await kraken.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await bot.send_file(
                kraken.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
        await eod(kraken, "**Error 404:**  Not Found")


@Andencento.on(andencento_cmd(pattern="meev(?: |$)(.*)", outgoing=True))
@Andencento.on(sudo_cmd(pattern="meev(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    user = kraken.pattern_match.group(1)
    if not user:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            await edit_or_reply(
                kraken,
                "`Sir please give some query to search and download it for you..!`",
            )
            return

    troll = await bot.inline_query("Myinstantsbot", f"{(deEmojify(user))}")
    if troll:
        await kraken.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await bot.send_file(
                kraken.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
        await eod(kraken, "**Error 404:**  Not Found")


CmdHelp("memevoice").add_command(
    "mev", "<query>", "Searches the given meme and sends audio if found."
).add_command("meev", "<query>", "Same as {hl}mev").add_info(
    "Audio Memes."
).add_warning(
    "✅ Harmless Module."
).add()
