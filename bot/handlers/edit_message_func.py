from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import MessageToEditNotFound, MessageToDeleteNotFound, MessageNotModified, BadRequest

from bot.db.db_interface import *
from bot.help_func.bot_func import bot


async def answer_callback(callback: types.CallbackQuery, new_text: str = None,
                          ikb: InlineKeyboardMarkup = None, photo: str = None) -> None:
    chat_id = callback.message.chat.id
    user = get_user(user_id=chat_id)
    msg_id = user['msg_id']

    await edit_message(chat_id=chat_id, msg_id=msg_id, new_text=new_text, ikb=ikb, photo=photo)
    await callback.answer()


async def answer_message(msg: types.Message, new_text: str = None,
                         ikb: InlineKeyboardMarkup = None, photo: str = None) -> None:
    user_id = msg.from_user.id
    user = get_user(user_id=user_id)
    chat_id = user['chat_id']
    msg_id = user['msg_id']
    await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)

    await edit_message(chat_id=chat_id, msg_id=msg_id, new_text=new_text, ikb=ikb, photo=photo)


async def edit_message(chat_id: int, msg_id: int, new_text: str = None,
                       ikb: InlineKeyboardMarkup = None, photo: str = None) -> None:
    if photo:
        try:
            new_photo = types.InputMediaPhoto(media=photo, caption=new_text)
            await bot.edit_message_media(media=new_photo, chat_id=chat_id, message_id=msg_id, reply_markup=ikb)

        except MessageToEditNotFound:
            new_msg = await bot.send_photo(chat_id=chat_id, photo=photo, caption=new_text, reply_markup=ikb)
            new_user(user_id=get_user_by_chat_id(chat_id), chat_id=new_msg.chat.id, msg_id=new_msg.message_id)

        except MessageNotModified:
            pass

        except BadRequest:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)

            except MessageToDeleteNotFound:
                pass

            new_msg = await bot.send_photo(chat_id=chat_id, photo=photo, caption=new_text, reply_markup=ikb)
            new_user(user_id=get_user_by_chat_id(chat_id), chat_id=new_msg.chat.id, msg_id=new_msg.message_id)

    else:
        try:
            await bot.edit_message_text(text=new_text, chat_id=chat_id, message_id=msg_id, reply_markup=ikb)

        except MessageToEditNotFound:
            new_msg = await bot.send_message(chat_id=chat_id, text=new_text, reply_markup=ikb)
            new_user(user_id=get_user_by_chat_id(chat_id), chat_id=new_msg.chat.id, msg_id=new_msg.message_id)

        except MessageNotModified:
            pass

        except BadRequest:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)

            except MessageToDeleteNotFound:
                pass

            new_msg = await bot.send_message(chat_id=chat_id, text=new_text, reply_markup=ikb)
            new_user(user_id=get_user_by_chat_id(chat_id), chat_id=new_msg.chat.id, msg_id=new_msg.message_id)

