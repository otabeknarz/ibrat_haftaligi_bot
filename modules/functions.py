import asyncio

import requests
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from . import settings


def get_request(url, *args, **kwargs) -> requests.Response:
    return requests.get(url, *args, **kwargs)


def post_request(url, json, *args, **kwargs) -> requests.Response:
    return requests.post(url, json=json, *args, **kwargs)


def patch_request(url, json, *args, **kwargs) -> requests.Response:
    return requests.patch(url, json=json, *args, **kwargs)


async def handle_start_with_invitation(bot: Bot, message: Message, parts):
    if len(parts) != 2:
        return

    invitation_token = parts[-1]
    response = post_request(
        url=settings.INVITATIONS_API,
        json={
            "invitation_token": invitation_token,
            "invited_user_id": message.from_user.id,
        },
    )
    if response.ok:
        json_response = response.json()

        invited_by_id = json_response.get("invited_by")
        invited_user_id = json_response.get("invited_user")

        invited_user_response = get_request(
            url=f"{settings.USERS_API}{invited_user_id}/"
        )
        if invited_user_response.ok:
            invited_user_json = invited_user_response.json()
            invited_user_username = invited_user_json.get("username")

            if invited_user_username.isdigit():
                invited_user_name = f"{invited_user_json.get("first_name")} {invited_user_json.get("last_name")}"
                await bot.send_message(
                    invited_by_id, f"🥳 Tabriklaymiz! Siz {invited_user_name} ni taklif qildingiz."
                )
            else:
                await bot.send_message(
                    invited_by_id,
                    f"🥳 Tabriklaymiz! Siz @{invited_user_username} ni taklif qildingiz.",
                )

        else:
            await bot.send_message(
                invited_by_id, "🥳 Tabriklaymiz!, Siz yana bir do'stingizni taklif qildingiz"
            )

        # Checking and sending a link to the user who has invited people
        await asyncio.sleep(1)
        invited_by_response = get_request(url=f"{settings.USERS_API}{invited_by_id}/")
        if invited_by_response.ok:
            invited_by_json = invited_by_response.json()
            if (
                not invited_by_json.get("has_taken_gift")
                and len(invited_by_json.get("invitations", []))
                == settings.USERS_SHOULD_INVITE_COUNT
            ):
                await bot.send_message(
                    invited_by_id,
                    """🙌🏻 <b>Barakalla, siz buni uddaladingiz!</b>

🤩 Siz shartni to'liq bajarib, 7 ta do'stingizni loyihaga taklif qilib <b>"Ibrat haftaligi – 7 kun, 7 yangi marra"</b> ning rasman qatnashchisiga aylandingiz!

• Endi siz <b><i>7 kun</i></b> davomida quyidagi spikerlar bilan bo'lib o'tadigan onlayn jonli va eng muhimi manfaatli suhbatlarda ishtirok eta olasiz:

<blockquote><i>• <b>Xushnudbek Xudoyberdiyev</b> – huquqshunos;
• <b>Shoxrux Olimov</b> – CELTA sertifikati va IELTS 8.5 sohibi;
• <b>Otabek Mahkamov</b> – huquqshunos, bloger va jurnalist;
• <b>Alisher Sa'dullayev</b> – Yoshlar ishlari agentligi direktori;
• <b>Rustam Qoriyev</b> – "Ibrat Farzandlari" loyiha rahbari;
• <b>Shohida Ibragimova</b> – moliyachi;
• <b>Aziz Rahimov</b> – "Rahimov school" asoschisi</i></blockquote>

🎁 Marhamat:""",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="🎯 Ishtirok etish",
                                    url="https://t.me/+5H5gCc1MxO5iYzUy",
                                )
                            ]
                        ]
                    ),
                )
                patch_request(
                    url=f"{settings.USERS_API}{invited_by_id}/",
                    json={"has_taken_gift": True},
                )
