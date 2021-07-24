import datetime
import io
import traceback

from selenium import webdriver

from . import *


@Andencento.on(andencento_cmd(pattern="(webshot|screenshot) (.*)", outgoing=True))
@Andencento.on(sudo_cmd(pattern="(webshot|screenshot) (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if Config.GOOGLE_CHROME_BIN is None:
        await eod(event, "need to install Google Chrome. Module Stopping.")
        return
    user = await eor(event, "Processing ...weit")
    start = datetime.datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = Config.GOOGLE_CHROME_BIN
        await user.edit("Starting Google Chrome BIN")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        input_str = event.pattern_match.group(1)
        driver.get(input_str)
        await user.edit("Calculating Page Dimensions")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        await user.edit("Painting web-page")
        driver.set_window_size(width + 100, height + 100)
        im_png = driver.get_screenshot_as_png()
        driver.close()
        await user.edit("Stopping Google Chrome BIN")
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        with io.BytesIO(im_png) as out_file:
            out_file.name = "Andencento .ScreenCapture.PNG"
            await bot.send_file(
                event.chat_id,
                out_file,
                caption=input_str,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True,
            )
        end = datetime.datetime.now()
        ms = (end - start).seconds
        await user.edit(f"Completed screencapture Process in {ms} seconds")
    except Exception:
        await eod(user, traceback.format_exc())


CmdHelp("capture").add_command(
    "screenshot",
    "<link>",
    "Gives out the web screenshot of given link via Google Crome Bin in .png format",
    ".screenshot https://github.com/userboy-op/userbot",
).add_command("webshot", "<link>", f"Same as  {hl}screenshot.").add_info(
    "Website Screenshot Maker."
).add_warning(
    "✅ Harmless Module."
).add()
