from aiogram import Bot
from dotenv import load_dotenv
import os


logo_photo = 'AgACAgIAAxkBAAID-2RVBP5FgniQ-5CahY1LJ4jjYFlQAAIVxjEbMqipSs1ynQT0PoXZAQADAgADcwADLwQ'

load_dotenv('.env')
token = os.getenv("TOKEN_API")
bot = Bot(token)


async def get_username(chat_id: int):
    chat = await bot.get_chat(chat_id=chat_id)
    username = f"@{chat.username}"

    return username