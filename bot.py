import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from dotenv import load_dotenv

from keep_alive import keep_alive

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GAME_URL = os.getenv("GAME_URL", "https://t.me/nightdriving3d_bot?startapp=game_heart")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

CAPTION = (
    "<b>🌃 Night Drive 3D</b> — ночной симулятор вождения с неоновыми огнями города, "
    "дождём и басами твоей музыки.\n\n"
    "🚦 <b>Выбирай режим:</b> город со светофорами и трафиком, «Закон» с полицией, "
    "камерами и штрафами, пустой город, трасса, лесная трасса или погоня, где нужно "
    "уйти от патруля.\n\n"
    "💰 Зарабатывай деньги за каждый проеханный километр, покупай новые машины и "
    "прокачивай их в гараже: меняй цвет, тонировку, посадку, подсветку и фары.\n\n"
    "🚶 Можно выйти из машины и прогуляться пешком, посмотреть на авто снаружи и "
    "поменять погоду.\n\n"
    "🎵 Загрузи свою музыку — бас раскачает свет, город и камеру.\n\n"
    "🎮 Управляй рулём на экране, наклоном телефона или кнопками, выбирай автомат "
    "или механику. Три уровня графики подходят и для слабых устройств."
)


def game_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🚗 Открыть игру", url=GAME_URL)]]
    )


@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Указываем путь к локальному файлу
    gif_path = "nightdrive.gif"
    
    if os.path.exists(gif_path):
        try:
            # Загружаем локальный файл
            animation = FSInputFile(gif_path)
            await message.answer_animation(
                animation=animation,
                caption=CAPTION,
                reply_markup=game_keyboard(),
            )
            return
        except Exception as e:
            logging.warning(f"Не удалось отправить локальный GIF: {e}")
    
    # Если файла нет или произошла ошибка — отправляем просто текст
    await message.answer(text=CAPTION, reply_markup=game_keyboard())


@dp.message(F.text == "/game")
async def cmd_game(message: Message):
    await message.answer(
        "🌃 <b>Night Drive 3D</b>\nЖми кнопку ниже и погнали!",
        reply_markup=game_keyboard(),
    )


@dp.message(F.text == "/health")
async def cmd_health(message: Message):
    await message.answer("✅ Бот работает.")


async def main():
    keep_alive()  # Поднимаем HTTP-сервер для Render
    logging.info("Bot starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
