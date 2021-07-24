import os

from userbot import YOUR_NAME as ALIVE_NAME
ver = "0.2"

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Unknown"
PM_IMG = (
    os.environ.get("ALIVE_PIC", None)
    or "https://telegra.ph/file/3d208ecf6d0ea9389d8f8.jpg"
)
pm_caption = "➥ **αη∂єη¢єηтσ:** `ONLINE`\n\n"
pm_caption += "➥ **ѕуѕтємѕ ѕтαтѕ**\n"
pm_caption += "➥ **тєℓєтнση νєяѕιση:** `1.23.0` \n"
pm_caption += "➥ **ρутнση:** `3.9.6` \n"
pm_caption += "➥ **∂αтαвαѕє ѕтαтυѕ:**  `Functional`\n"
pm_caption += "➥ **¢υяяєηт вяαη¢н** : `Andencento`\n"
pm_caption += f"➥ **νєяѕιση** : `{ver}`\n"
pm_caption += f"➥ **му вσѕѕ** : {DEFAULTUSER} \n"
pm_caption += f"➥ **ℓι¢єηѕє** : [𝘎𝘕𝘜 𝘈𝘧𝘧𝘦𝘳𝘰 𝘎𝘦𝘯𝘦𝘳𝘢𝘭 𝘗𝘶𝘣𝘭𝘪𝘤 𝘓𝘪𝘤𝘦𝘯𝘴𝘦 𝘷3.0](https://github.com/Andencento/Andencento/blob/Andencento/LICENSE/)\n"
pm_caption += "➥ **¢σρуяιgнт** : By [𝘛𝘦𝘢𝘮 𝘈𝘯𝘥𝘦𝘯𝘤𝘦𝘯𝘵𝘰](https://github.com/Andencento/Andencento/)\n"


# only Owner Can Use it
@Andencento.on(andencento_cmd(outgoing=True, pattern="alive$"))
@Andencento.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def _(event):
    await event.get_chat()
    await event.delete()
    await Andencento.send_file(event.chat_id, PM_IMG, caption=pm_caption)
