import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from routers import router as main_router
from config import settings


async def main():
    dp = Dispatcher()

    dp.include_router(main_router)

    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот закончил работу")