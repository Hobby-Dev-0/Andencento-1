"""
Made by GODBOYX
"""
import re
import os
from telethon import custom, Button, events
from userbot import bot, asst
from . import *
from userbot import YOUR_NAME as ALIVE_NAME

ver = "0.2"

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Unknown"
PM_IMG = (
    os.environ.get("ALIVE_PIC", None)
    or "https://telegra.ph/file/3d208ecf6d0ea9389d8f8.jpg"
)
pm_caption = "➥ αη∂єη¢єηтσ: ONLINE\n\n"
pm_caption += "➥ ѕуѕтємѕ ѕтαтѕ\n"
pm_caption += "➥ тєℓєтнση νєяѕιση: 1.23.0 \n"
pm_caption += "➥ ρутнση: 3.9.6 \n"
pm_caption += "➥ ∂αтαвαѕє ѕтαтυѕ:  Functional\n"
pm_caption += "➥ ¢υяяєηт вяαη¢н : Andencento\n"
pm_caption += f"➥ νєяѕιση : {ver}\n"
pm_caption += f"➥ му вσѕѕ : {DEFAULTUSER} \n"
pm_caption += f"➥ ℓι¢єηѕє : [𝘎𝘕𝘜 𝘈𝘧𝘧𝘦𝘳𝘰 𝘎𝘦𝘯𝘦𝘳𝘢𝘭 𝘗𝘶𝘣𝘭𝘪𝘤 𝘓𝘪𝘤𝘦𝘯𝘴𝘦 𝘷3.0](https://github.com/Andencento/Andencento/blob/Andencento/LICENSE/)\n"
pm_caption += "➥ ¢σρуяιgнт : By [𝘛𝘦𝘢𝘮 𝘈𝘯𝘥𝘦𝘯𝘤𝘦𝘯𝘵𝘰](https://github.com/Andencento/Andencento/)\n"
btn = [[custom.Button.inline("<<Deploy>>", data= "demploy")]]
btn += [[custom.Button.inline("<<String Session>>", data = "stling")]]
btn += [[Button.url("<<Repo>>", "https://github.com/Andencento/Andencento")]]


@asst.on(events.NewMessage(pattern=("/alive")))
async def _(event):
    await event.get_chat()
    await event.delete()
    await asst.send_file(event.chat_id, PM_IMG, caption=pm_caption, buttons=btn)



@asst.on(events.callbackquery.CallbackQuery(data=re.compile(b"demploy")))
async def demploy(event):
 bottm = [[Button.url("<Railway Deploy>", "https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2FAndencento%2FRailway-Deploy&plugins=postgresql&envs=YOUR_NAME%2CTZ%2CALIVE_PIC%2CPMPERMIT_PIC%2CPM_LOG_ID%2CHANDLER%2CBUTTONS_IN_HELP%2CTEMP_DOWNLOAD_DIRECTORY%2CPM_PERMIT%2CAPP_ID%2CAPI_HASH%2CLOGGER_ID%2CANDENCENTO_SESSION%2CBOT_TOKEN%2CTAG_LOGGER%2CBOT_USERNAME%2CSUDO_USERS&optionalEnvs=PM_LOG_ID%2CTAG_LOGGER%2CSUDO_USERS&YOUR_NAMEDesc=This+is+Alive+Name+So+Fill+it+Properly+It+is+Mandatory&TZDesc=Time+Zone+of+a+country+Dont+Edit+untill+you+want+diffrent+time+zone&ALIVE_PICDesc=Alive+Pic+Paste+Telegraph+Link&PMPERMIT_PICDesc=Pmpermit+Pic&PM_LOG_IDDesc=Fill+your+private+Channel+ID+if+you+want+to+Log+PM+messages.&HANDLERDesc=Your+command+handler.+Default+is+%27+.+%27+%28dot%29.&BUTTONS_IN_HELPDesc=No.of+buttons+to+display+in+help+menu.&TEMP_DOWNLOAD_DIRECTORYDesc=Temp+Storage+&PM_PERMITDesc=Defualt+is+Enable+if+You+Want+To+Disable+PMPERMIT+type+Disable&APP_IDDesc=Get+this+value+from+my.telegram.org+6+Digits+Value&API_HASHDesc=Get+this+value+from+my.telegram.org&LOGGER_IDDesc=Logger+Id+Starts+from+-100&ANDENCENTO_SESSIONDesc=Get+this+value+by+using+https%3A%2F%2Freplit.com%2F%40madboy482%2FSession-Andencento+and+fill+this+is+your+String+Session.&BOT_TOKENDesc=Make+a+bot+from+%40BotFather+and+paste+the+bot+token+here.&TAG_LOGGERDesc=Make+a+group+and+add+rose.+Do+%2Fid+and+paste+the+chat+id+here.+Make+Sure+id+Should+Start+From+-100&BOT_USERNAMEDesc=from+%40BotFather+Get+Bot+username+which+you+filled+token+and+paste+the+username+here.&SUDO_USERSDesc=Userid+of+user+to+grant+sudo+access.+Add+multiple+sudo+users+by+giving+a+space+between+userids&TZDefault=Asia%2FKolkata&HANDLERDefault=.&BUTTONS_IN_HELPDefault=7&TEMP_DOWNLOAD_DIRECTORYDefault=.%2Fuserbot%2Fcache&PM_PERMITDefault=ENABLE")], [Button.url("<Heroku Deploy>", "https://heroku.com/deploy?template=https://github.com/Andencento/Deploy-Andencento")]]

 bottm += [[Button.url("<VC Deploy>", "http://heroku.com/deploy?template=https://github.com/Andencento/Andencento/tree/vc")]]
 bottm += [[custom.Button.inline("<<Back", data="bamck")]]
 
 await event.edit("Welcome to Deployment Section", buttons=bottm)
 
@asst.on(events.callbackquery.CallbackQuery(data=re.compile(b"bamck")))
async def bamck(event):
    await event.edit(pm_caption, buttons=btn)
    
    
    
@asst.on(events.callbackquery.CallbackQuery(data=re.compile(b"stling")))
async def stling(event):
 batan = [[Button.url("<Andencento String Session>", "https://replit.com/@madboy482/Session-Andencento/")]]
 batan += [[Button.url("<VC String Session>", "https://replit.com/@dashezup/generate-pyrogram-session-string")]]
 batan += [[custom.Button.inline("<<Back", data="bomk")]]
 
 await event.edit("Welcome to String Session Section ", buttons=batan)
 
 
@asst.on(events.callbackquery.CallbackQuery(data=re.compile(b"bomk")))
async def bamck(event):
    await event.edit(pm_caption, buttons=btn)
