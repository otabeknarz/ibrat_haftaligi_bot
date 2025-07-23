import asyncio
import logging
import sys
from os import getenv

from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup

from modules import functions
from modules import settings
from modules.buttons import Buttons, InlineButtons
from modules.filters import TextEqualsFilter
from modules.functions import get_request
from modules.states import SendPostStates

load_dotenv()
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

buttons = Buttons()
inline_buttons = InlineButtons()

photo = FSInputFile("top-students.png")
get_welcome_text = (
    lambda join_link: f"""<b>📌 Avval qatnashib ko'ring, rahmatni keyin aytasiz!</b>

🎙 <b>"Ibrat haftaligi – 7 kun, 7 yangi marra"</b> da siz 7 kun davomida 7 xil soha vakillari bilan tashkillashtirilgan manfaatli suhbatlarda qatnashib, savollaringizga javob olasiz:

<blockquote><i>• <b>Xushnudbek Xudoyberdiyev</b> – huquqshunos;
• <b>Shoxrux Olimov</b> – CELTA sertifikati va IELTS 8.5 sohibi;
• <b>Otabek Mahkamov</b> – huquqshunos, bloger va jurnalist;
• <b>Alisher Sa'dullayev</b> – Yoshlar ishlari agentligi direktori;
• <b>Rustam Qoriyev</b> – "Ibrat Farzandlari" loyiha rahbari;
• <b>Shohida Ibragimova</b> – moliyachi;
• <b>Aziz Rahimov</b> – "Rahimov school" asoschisi</i></blockquote>

🤩 Bundan tashqari, eng faol targ'ibotchi sifatida <b><i>6.500.000 so'mgacha pul mukofotlari, shuningdek, 150 dan ortiq bonusli sovg'alar, premium til kurslari</i></b>ni yutib olish imkoniga ega bo'lasiz.

<b>🙌🏻 Qatnashish – mutlaqo BEPUL.</b>

https://t.me/ibrat_haftaligi_bot?start={join_link}
"""
)


async def check_is_subscribed(chat_id, user_id) -> bool:
    try:
        status = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return status.status != "left"
    except Exception as e:
        logger.error(e)
        return False


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_json = {
        "id": message.from_user.id,
        "username": message.from_user.username or message.from_user.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name or "",
    }
    response = functions.post_request(url=settings.USERS_API, json=user_json)

    if response.ok:
        parts = message.text.strip().split(maxsplit=1)
        await functions.handle_start_with_invitation(
            bot=bot, message=message, parts=parts
        )

        unjoined_channels_inline_buttons = inline_buttons.get_join_channel_buttons(settings.CHANNELS_IDs)
        await message.answer(
        """🔥 <b>"Ibrat haftaligi – 7 kun, 7 yangi marra"</b> da ishtirok etish uchun bizning rasmiy sahifalarimizga obuna bo'ling va ilovamizni yuklab oling.

<b>"Ibrat Academy"</b> – tillarni tez, oson va samarali o'rgatishga mo'ljallangan yagona onlayn ta'lim platformasi

Keyin <b>"Obuna bo'ldim✅"</b> tugmasini bosing:""",
            reply_markup=unjoined_channels_inline_buttons,
        )
    else:
        response = functions.get_request(
            url=f"{settings.USERS_API}{message.chat.id}/"
        )

        json_response = response.json()
        await message.answer(f"Sizda <b>{len(json_response.get('invitations'))}</b> ball bor")


@dp.message(TextEqualsFilter("📊 Natijalarim"))
async def my_stats_handler(message: Message) -> None:
    response = functions.get_request(url=f"{settings.USERS_API}{message.from_user.id}/")
    stats_response = functions.get_request(url=settings.STATS_API)
    if response.ok and stats_response.ok:
        json_response = response.json()
        json_stats_response = stats_response.json()
        stats = ""
        for key, stat in enumerate(json_stats_response, start=1):
            username = (stat.get("username", "1"), stat.get("username", "1").isdigit())
            stats += f"{key}. <b>{stat.get('first_name') + stat.get('last_name', '') if username[1] else "@" + username[0]}</b> - <b>{stat.get("invitations_count")}</b>\n"
        await message.answer(
            f"""🎯 <b>Eng ko'p ball to'plagan faol ishtirokchilar ro'yxati:</b>

Sizning natijangiz: <b>{len(json_response.get('invitations', []))}</b>


{stats}

📌 Eslatib o'tamiz, eng faol ilk 200 ta ishtirokchiga quyidagi sovg'alar topshiriladi:

🥇<b>1-o'rin:</b> 3 million so'm
🥈<b>2-o'rin:</b> 2 million so'm
🥉<b>3-o'rin:</b> 1 million so'm
🎖<b>4-o'rin:</b> 500 ming so'm pul mukofotlari

• <b>5-20-o'rin</b> – Rustam Qoriyevning mualliflik kitoblari;
• <b>21-40-o'rin</b> – "Super Start" beginner;
• <b>41-60-o'rin</b> – "Super Start" elementary;
• <b>61-80-o'rin</b> – "Tezkor Turk tili" 
• <b>81-100-o'rin</b> – "Tezkor Rus tili" qiymati 159.000 so'mga teng bo'lgan 3 oylik premium til kurslari;

• <b>101-120-o'rin</b> – 40% lik chegirma;
• <b>121-160-o'rin</b> – 30% lik chegirma;
• <b>161-200-o'rin</b> – 20% lik chegirma taqdim qilinadi.

✅ Sizda - ball mavjud va siz - o'rindasiz. Yanada ko'proq ball to'plashda davom eting!

*G'oliblar 21-iyul, 19:00 da aniqlanadi.""",
            reply_markup=buttons.main_keyboard()
        )
    else:
        await message.answer(
            "Qandaydir muammo yuz berdi biz bilan bog'laning (skringshotlarni yuborishni unutmang @otabke_narz)",
            reply_markup=buttons.remove_keyboard,
        )


@dp.callback_query()
async def all_callback_handler(callback: CallbackQuery) -> None:
    query = callback.data

    if query == "joined":
        subscription_statuses = {True: {}, False: {}}
        for channel_id, (channel_name, channel_link) in settings.CHANNELS_IDs.items():
            status = await check_is_subscribed(channel_id, callback.message.chat.id)
            subscription_statuses[status].update(
                {channel_id: (channel_name, channel_link)}
            )

        if subscription_statuses.get(False):
            unjoined_channels_inline_buttons = inline_buttons.get_join_channel_buttons(
                subscription_statuses.get(False)
            )
            await callback.message.delete()
            await asyncio.sleep(1)
            await callback.message.answer(
                """😊 <b>"Ibrat haftaligi – 7 kun, 7 yangi marra"</b> da ishtirok etish uchun bizning rasmiy sahifalarimizga obuna bo'ling va ilovamizni yuklab oling.

"Ibrat Academy" – tillarni tez, oson va samarali o'rgatishga mo'ljallangan yagona onlayn ta'lim platformasi

Keyin "Obuna bo'ldim✅" tugmasini bosing:""",
                reply_markup=unjoined_channels_inline_buttons,
            )

        else:
            await callback.message.answer("""⚡️ <b>"Ibrat Academy" — 22 dan ortiq tillarni istalgan vaqt va makonda mustaqil o'rganing!</b>

🫱🏻‍🫲🏻 Pastdagi havola orqali ilovani yuklab olishingiz mumkin. Marhamat:

https://onelink.to/ibratfarzandlari""")

            await asyncio.sleep(1)

            await callback.message.answer("""😉 <b>Tabriklayman! "Ibrat haftaligi – 7 kun, 7 yangi marra" ga xush kelibsiz!</b>

Xo'sh, diqqat bilan o'qing!

💯 Marafonda qatnashish mutlaqo bepul va loyihamizning ko'proq odamga foydasi tegishi uchun aynan sizning yordamingiz kerak bo'ladi.

<blockquote><i>✅ <b>Sharti:</b> bot sizga taqdim qilgan maxsus link orqali <b>7 ta do'stingizni</b> loyihamizga taklif qilasiz va avtomatik tarzda loyihada ishtirok etishingiz uchun maxsus linkni qabul qilib olasiz.

📌 <b>Unutmang, taklif postingiz orqali to'liq ro'yxatdan o'tgan har bir do'stingiz uchun sizga +1 ball beriladi.</b>

🤫 Va bu hali hammasi emas, agar siz eng faol targ'ibotchi bo'lishni maqsad qilsangiz, pul mukofotlari va boshqa ko'plab premium til kurslarini yutib olish imkoniga ega bo'lasiz!</i></blockquote>

Unga ko'ra, eng ko'p odam taklif qilgan faol targ'ibotchilar:

🥇<b>1-o'rin:</b> 3 million so'm
🥈<b>2-o'rin:</b> 2 million so'm
🥉<b>3-o'rin:</b> 1 million so'm
🎖<b>4-o'rin:</b> 500 ming so'm pul mukofotlari

• <b>5-20-o'rin</b> – Rustam Qoriyevning mualliflik kitoblari;
• <b>21-40-o'rin</b> – "Super Start" beginner;
• <b>41-60-o'rin</b> – "Super Start" elementary;
• <b>61-80-o'rin</b> – "Tezkor Turk tili" 
• <b>81-100-o'rin</b> – "Tezkor Rus tili" qiymati 159.000 so'mga teng bo'lgan 3 oylik premium til kurslari;

• <b>101-120-o'rin</b> – 40% lik chegirma;
• <b>121-160-o'rin</b> – 30% lik chegirma;
• <b>161-200-o'rin</b> – 20% lik chegirma taqdim qilinadi.

❗️ Esingizda bo'lsin, loyihada birinchi bo'lib <b>7 ta</b> do'stini taklif qilgan dastlabki <b>7000 ta</b> ishtirokchidan so'ng marafonga <b>START</b> beriladi va boshqa talabgorlar qabul qilinmaydi.

🫱🏻‍🫲🏻 Ko'p o'ylanmasdan, hoziroq taklif postingizni qabul qilib oling:""", reply_markup=inline_buttons.invitation_buttons)

    elif query == "invitation":
        response = functions.get_request(
                url=f"{settings.USERS_API}{callback.message.chat.id}/"
            )
        if not response.ok:
            response = functions.get_request(
                url=f"{settings.USERS_API}{callback.message.chat.id}/"
            )

        json_response = response.json()
        await callback.message.answer_photo(
            photo=photo,
            caption=get_welcome_text(json_response.get("invitation_token")),
            reply_markup=inline_buttons.get_participate_button(json_response.get("invitation_token")),
        )
        await asyncio.sleep(1)
        await callback.message.answer(
            """🎉 <b>Sizga berilgan postni do'stlaringiz bilan ulashing.</b>

• 7 ta do'stingiz sizning taklif havolangiz orqali botga <b>START</b> berib, to'liq obuna shartlarini bajarsa, sizga marafon bo'ladigan kanal uchun bir martalik link beriladi.""", reply_markup=buttons.main_keyboard()
        )

@dp.message(TextEqualsFilter("send_post_to_everyone"))
async def send_post_to_everyone(message: Message, state: FSMContext):
    if message.from_user.id not in settings.ADMINS.keys():
        return

    await message.answer(f"Eeee assalomu alaykum {settings.ADMINS[message.from_user.id]}, nima tashash kere odamlaga, tasheng!", buttons.cancel_posting)
    await state.set_state(SendPostStates.post)


@dp.message(SendPostStates.post)
async def send_post_to_everyone(message: Message, state: FSMContext):
    if message.from_user.id not in settings.ADMINS.keys():
        return

    if message.text == "Iiii to'xta bekor qil":
        await message.answer("Ha bo'ldi bo'ldi otmen qildim xavotir omeng...", reply_markup=buttons.remove_keyboard)
        await state.clear()
        return

    users_response = get_request(settings.USERS_API)
    if not users_response.ok:
        await message.answer("Serverda xatolik boldi uzur")
        await state.clear()
        return

    users = users_response.json()
    for user in users:
        try:
            await message.copy_to(user.get("id"))
        except Exception as e:
            logger.error(e)

        await asyncio.sleep(0.5)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
