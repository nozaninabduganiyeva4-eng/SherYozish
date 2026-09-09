import os
import sys
import html
import logging
import asyncio
from dotenv import load_dotenv

# Telegram bot kutubxonasi (aiogram 3.x)
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode, ChatAction
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# OpenAI rasmiy asinxron mijozi
from openai import AsyncOpenAI

# .env faylidagi o'zgaruvchilarni yuklash
load_dotenv()

# Tokenlar (.env dan olinadi)
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# OpenAI mijozini ishga tushirish
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# AI uchun maxsus tizimli ko'rsatma (Qisqa va ta'sirli she'r yaratish)
POEM_SYSTEM_PROMPT = (
    "Siz nozikta'b va iste'dodli o'zbek shoirisiz. "
    "Foydalanuvchi yuborgan so'z yoki mavzuga moslab QISQA, ixcham, qofiyalangan va chuqur ma'noli she'r yozing.\n"
    "Talablar:\n"
    "1. She'r juda ixcham bo'lsin: aniq 1 yoki 2 ta to'rtlik (jami 4 yoki 8 qator).\n"
    "2. O'zbek adabiy tilida, ajoyib qofiya va vaznga ega bo'lsin.\n"
    "3. Boshida mavzuga mos bitta chiroyli sarlavha qo'ying.\n"
    "4. Javobda faqat sarlavha va she'r matnini bering, ortiqcha salom-alik yoki izoh qo'shmang."
)


async def generate_short_poem(topic: str) -> str:
    """
    Foydalanuvchi yuborgan so'z yoki mavzuga qisqa she'r to'qiydi (4-8 qator).
    """
    if not OPENAI_API_KEY or not openai_client:
        return (
            "⚠️ <b>OpenAI API kaliti topilmadi!</b>\n\n"
            "Iltimos, <code>.env</code> faylida <code>OPENAI_API_KEY</code> ni to'g'ri ko'rsating."
        )

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": POEM_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Mavzu yoki so'z: {topic.strip()}\nIltimos, shu mavzuda 1-2 to'rtlikdan iborat go'zal va qisqa she'r to'qib bering."
                }
            ],
            temperature=0.8,
            max_tokens=350
        )

        poem = response.choices[0].message.content
        return poem.strip() if poem else "She'r yaratib bo'lmadi, qayta urinib ko'ring."

    except Exception as e:
        logger.error(f"OpenAI API xatoligi: {e}")
        err_msg = str(e).lower()
        if "quota" in err_msg or "insufficient" in err_msg:
            return "⚠️ OpenAI hisobingizda mablag' (quota) tugagan yoki chegaralangan. Iltimos, hisobingizni tekshiring."
        elif "api_key" in err_msg or "authentication" in err_msg:
            return "⚠️ OpenAI API kaliti noto'g'ri ko'rsatilgan. <code>.env</code> faylini tekshiring."
        return f"⚠️ Kechirasiz, she'r to'qishda xatolik yuz berdi: {html.escape(str(e))}"


def get_poem_keyboard(topic: str) -> InlineKeyboardMarkup:
    """She'r ostidagi qulay tugmalar"""
    # Callback ma'lumotining uzunligi 64 baytdan oshmasligi kerak
    safe_topic = topic[:30]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔁 Yana boshqa she'r", callback_data=f"regen:{safe_topic}")
            ],
            [
                InlineKeyboardButton(text="🌸 Bahor", callback_data="preset:Bahor"),
                InlineKeyboardButton(text="❤️ Muhabbat", callback_data="preset:Muhabbat"),
                InlineKeyboardButton(text="👩 Ona", callback_data="preset:Ona"),
            ],
            [
                InlineKeyboardButton(text="🤝 Do'stlik", callback_data="preset:Do'stlik"),
                InlineKeyboardButton(text="🇺🇿 Vatan", callback_data="preset:Vatan"),
                InlineKeyboardButton(text="🌧 Yomg'ir", callback_data="preset:Yomg'ir"),
            ]
        ]
    )
    return keyboard


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Boshlang'ich tavsiya etilgan mavzular tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌸 Bahor", callback_data="preset:Bahor"),
                InlineKeyboardButton(text="❤️ Muhabbat", callback_data="preset:Muhabbat"),
                InlineKeyboardButton(text="👩 Ona", callback_data="preset:Ona"),
            ],
            [
                InlineKeyboardButton(text="🤝 Do'stlik", callback_data="preset:Do'stlik"),
                InlineKeyboardButton(text="🇺🇿 Vatan", callback_data="preset:Vatan"),
                InlineKeyboardButton(text="🌧 Yomg'ir", callback_data="preset:Yomg'ir"),
            ]
        ]
    )
    return keyboard


# Bot va Dispatcher sozlamalari
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN aniqlanmadi! .env faylida BOT_TOKEN ni kiriting.")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# /start komandasi
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name if message.from_user else "Do'stim"
    text = (
        f"Assalomu alaykum, <b>{html.escape(user_name)}</b>! ✍️✨\n\n"
        "Men <b>She'r Yaratuvchi AI</b> botiman.\n\n"
        "Menga istalgan <b>bitta so'z</b> yoki <b>mavzuni</b> yozib yuboring (yoki quyidagi tugmalardan birini bosing), "
        "men sizga shu mavzuda <b>qisqa, jarangdor va qofiyali to'rtlik</b> to'qib beraman!\n\n"
        "💡 <i>Masalan: Ona, Muhabbat, Hayot, Baxt, Qalb, Sog'inch...</i>"
    )
    await message.answer(text, reply_markup=get_start_keyboard())


# /help komandasi
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    text = (
        "💡 <b>Botdan qanday foydalaniladi?</b>\n\n"
        "1. Shunchaki o'zingiz xohlagan mavzu yoki so'zni xabar qilib yuboring.\n"
        "2. Bot sun'iy intellekt (AI) yordamida shu so'zga atab original to'rtlik yozadi.\n"
        "3. <b>«🔁 Yana boshqa she'r»</b> tugmasi orqali shu mavzuda yangi variant to'qishingiz mumkin.\n"
        "4. Bot buyruqlari: /start va /help"
    )
    await message.answer(text)


async def send_poem_to_chat(chat_id: int, topic: str):
    """Mavzu bo'yicha she'r to'qib yuboruvchi yordamchi funksiya"""
    await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    wait_msg = await bot.send_message(
        chat_id=chat_id,
        text=f"⏳ <i>«{html.escape(topic)}» haqida she'r to'qilmoqda...</i>"
    )

    poem = await generate_short_poem(topic)

    try:
        await wait_msg.delete()
    except Exception:
        pass

    result_text = (
        f"📖 <b>«{html.escape(topic)}»</b>\n\n"
        f"{html.escape(poem)}\n\n"
        f"✍️ <i>Boshqa biror so'z yuborishingiz yoki tugmalardan tanlashingiz mumkin!</i>"
    )
    await bot.send_message(chat_id=chat_id, text=result_text, reply_markup=get_poem_keyboard(topic))


# Matnli xabarlarni qabul qilish
@dp.message(F.text)
async def handle_topic(message: types.Message):
    topic = message.text.strip()

    if len(topic) > 120:
        await message.answer("⚠️ Iltimos, so'z yoki mavzuni qisqaroq qilib yuboring (maksimal 120 belgi).")
        return

    await send_poem_to_chat(message.chat.id, topic)


# Callback tugmalar (Qayta to'qish yoki tayyor mavzular)
@dp.callback_query(F.data.startswith("regen:"))
async def callback_regen(query: CallbackQuery):
    topic = query.data.split(":", 1)[1]
    await query.answer("Yangi she'r to'qilmoqda...")
    if query.message:
        await send_poem_to_chat(query.message.chat.id, topic)


@dp.callback_query(F.data.startswith("preset:"))
async def callback_preset(query: CallbackQuery):
    topic = query.data.split(":", 1)[1]
    await query.answer(f"«{topic}» mavzusi tanlandi")
    if query.message:
        await send_poem_to_chat(query.message.chat.id, topic)


async def main():
    logger.info("She'r yaratuvchi Telegram bot ishga tushmoqda...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi!")

