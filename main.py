import asyncio
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.handlers.register_handlers import register_handlers
from bot.db.sqlite import db_start
from bot.help_func.bot_func import bot


def register_handler(dp: Dispatcher) -> None:
    register_handlers(dp=dp)


async def main() -> None:
    db_start()

    storage = MemoryStorage()

    dp = Dispatcher(bot, storage=storage)

    register_handler(dp=dp)

    try:
        await dp.start_polling()
    except Exception as _ex:
        pass


if __name__ == "__main__":
    asyncio.run(main())