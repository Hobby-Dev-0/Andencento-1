import asyncio
import io
import os

from . import *

andencento_logo = "https://telegra.ph/file/c70894d968a5823d04f0e.png"
Andencento_logo = andencento_logo


@bot.on(andencento_cmd(pattern=r"cmds"))
@bot.on(sudo_cmd(pattern=r"cmds", allow_sudo=True))
async def kk(event):
    if event.fwd_from:
        return
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    cmd = "ls plugins"
    process = await asyncio.create_subprocess_sandencento(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    _o = o.split("\n")
    o = "\n".join(_o)
    OUTPUT = f"List of Plugins in bot :- \n\n{o}\n\n<><><><><><><><><><><><><><><><><><><><><><><><>\nHELP:- If you want to know the commands for a plugin, do :- \n.plinfo <plugin name> without the < > brackets. \nJoin {Eiva_grp} for help."
    if len(OUTPUT) > 69:
        thumb = andencento_logo
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "cmd_list.text"
            andencento_file = await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                thumb=thumb,
                reply_to=reply_to_id,
            )
            await edit_or_reply(
                andencento_file,
                f"Output Too Large. This is the file for the list of plugins in bot.\n\n**BY :-** {Andencento_USER}",
            )
            await event.delete()


@bot.on(andencento_cmd(pattern=r"send (?P<shortname>\w+)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"send (?P<shortname>\w+)", allow_sudo=True))
async def send(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    input_str = event.pattern_match.group(1)
    omk = f"**• Plugin name ≈** `{input_str}`\n**• Uploaded by ≈** {Andencento_mention}\n\n⚡ **[ɛɢɛռɖαʀʏ ᴀғ Andencento]({chnl_link})** ⚡"
    the_plugin_file = "./plugins/{}.py".format(input_str)
    if os.path.exists(the_plugin_file):
        thumb = Andencento_logo
        lauda = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            thumb=thumb,
            caption=omk,
            force_document=True,
            allow_cache=False,
            reply_to=message_id,
        )
        await event.delete()
    else:
        await eod(event, "File not found..... Kek")


@bot.on(andencento_cmd(pattern=r"remove (?P<shortname>\w+)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"remove (?P<shortname>\w+)", allow_sudo=True))
async def uninstall(kraken):
    if kraken.fwd_from:
        return
    shortname = kraken.pattern_match["shortname"]
    dir_path = f"./plugins/{shortname}.py"
    try:
        remove_plugin(shortname)
        os.remove(dir_path)
        await eod(kraken, f"removed `{shortname}` successfully")
    except OSError as e:
        await kraken.edit("Error: %s : %s" % (dir_path, e.strerror))


@bot.on(andencento_cmd(pattern=r"unload (?P<shortname>\w+)$"))
@bot.on(sudo_cmd(pattern=r"unload (?P<shortname>\w+)$", allow_sudo=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await event.edit(f"Successfully unloaded `{shortname}`")
    except Exception as e:
        await event.edit(
            "Successfully unloaded {shortname}\n{}".format(shortname, str(e))
        )


@bot.on(andencento_cmd(pattern=r"load (?P<shortname>\w+)$"))
@bot.on(sudo_cmd(pattern=r"load (?P<shortname>\w+)$", allow_sudo=True))
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await event.edit(f"Successfully loaded `{shortname}`")
    except Exception as e:
        await event.edit(
            f"Sorry, could not load {shortname} because of the following error.\n{str(e)}"
        )


CmdHelp("core").add_command(
    "install",
    "<reply to a .py file>",
    "Installs the replied python file if suitable to Andencento's codes.",
).add_command(
    "remove",
    "<plugin name>",
    "Uninstalls the given plugin from єιναϐοτ. To get that again do .restart",
    "uninstall alive",
).add_command(
    "load", "<plugin name>", "Loades the unloaded plugin to your userbot", "load alive"
).add_command(
    "unload", "<plugin name>", "Unloads the plugin from your userbot", "unload alive"
).add_command(
    "send",
    "<file name>",
    "Sends the given file from your userbot server, if any.",
    "send alive",
).add_command(
    "cmds", None, "Gives out the list of modules in AndencentoBot."
).add_warning(
    "❌ Install External Plugin On Your Own Risk. We won't help if anything goes wrong after installing a plugin."
).add()
