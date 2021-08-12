import asyncio

from . import *

SUDO_WALA = Config.SUDO_USERS
lg_id = Config.LOGGER_ID


@Andencento.on(andencento_cmd(pattern="spam (.*)"))
@Andencento.on(sudo_cmd(pattern="spam (.*)", allow_sudo=True))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[6:8])
        spam_message = str(e.text[8:])
        await asyncio.wait([e.respond(spam_message) for i in range(counter)])
        await e.delete()
        await e.client.send_message(
            lg_id, f"#SPAM \n\nSpammed  `{counter}`  messages!!"
        )


@Andencento.on(andencento_cmd(pattern="bigspam"))
@Andencento.on(sudo_cmd(pattern="bigspam", allow_sudo=True))
async def bigspam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[9:13])
        spam_message = str(e.text[13:])
        for i in range(1, counter):
            await e.respond(spam_message)
        await e.delete()
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP, "#BIGSPAM \n\n" "Bigspam was executed successfully"
            )


@Andencento.on(andencento_cmd("dspam (.*)"))
@Andencento.on(sudo_cmd(pattern="dspam (.*)", allow_sudo=True))
async def spammer(e):
    if e.fwd_from:
        return
    input_str = "".join(e.text.split(maxsplit=1)[1:])
    spamDelay = float(input_str.split(" ", 2)[0])
    counter = int(input_str.split(" ", 2)[1])
    spam_message = str(input_str.split(" ", 2)[2])
    await e.delete()
    for _ in range(counter):
        await e.respond(spam_message)
        await asyncio.sleep(spamDelay)


@Andencento.on(andencento_cmd(pattern="mspam (.*)"))
@Andencento.on(sudo_cmd(pattern="mspam (.*)", allow_sudo=True))
async def tiny_pic_spam(e):
    await e.get_sender()
    await e.client.get_me()
    try:
        await e.delete()
    except BaseException:
        pass
    try:
        counter = int(e.pattern_match.group(1).split(" ", 1)[0])
        reply_message = await e.get_reply_message()
        if (
            not reply_message
            or not e.reply_to_msg_id
            or not reply_message.media
            or not reply_message.media
        ):
            return await e.edit("```Reply to a pic/sticker/gif/video message```")
        message = reply_message.media
        for i in range(1, counter):
            await e.client.send_file(e.chat_id, message)
    except BaseException:
        return await e.reply(
            f"**Error**\nUsage `{hl}mspam <count> reply to a sticker/gif/photo/video`"
        )


CmdHelp("spam").add_command(
    "spam", "<number> <text>", "Sends the text 'X' number of times.", ".spam 99 Hello"
).add_command(
    "mspam",
    "<reply to media> <number>",
    "Sends the replied media (gif/ video/ sticker/ pic) 'X' number of times",
    ".mspam 100 <reply to media>",
).add_command(
    "dspam",
    "<delay> <spam count> <text>",
    "Sends the text 'X' number of times in 'Y' seconds of delay",
    ".dspam 5 100 Hello",
).add_command(
    "bigspam",
    "<count> <text>",
    "Sends the text 'X' number of times. This what userbot iz known for. The Best BigSpam Ever",
    ".bigspam 5000 Hello",
).add_info(
    "Spammers Commands"
).add_warning(
    "❌ May Get Floodwait Error Or Limit Your Account"
).add()
