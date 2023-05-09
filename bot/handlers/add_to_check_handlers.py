from aiogram import types, Dispatcher

from bot.keyboards.user_keyboards import *
from bot.states_groups.states_groups import *
from bot.db.db_interface import *
from bot.handlers.edit_message_func import answer_message
from bot.handlers.main_handlers import callback_or_message_start


async def message_add_to_check(msg: types.Message) -> None:
    valid = is_check_in_db(msg.text)
    if valid:
        if not is_check_owner(user_id=msg.from_user.id, check_id=msg.text):
            if not is_conn_in_db(user_id=msg.from_user.id, check_id=msg.text):
                new_conn(user_id=msg.from_user.id, check_id=msg.text)
                text = 'Вы успешно добавились в чек'
            else:
                text = 'Вы уже добавились в этот чек'
        else:
            text = 'Вы не можете добавиться в свой чек'
        await callback_or_message_start(msg=msg, text=text)
        await MainMenuStatesGroup.main_menu.set()
    else:
        new_text = 'Чек с таким ID не найден.\n\nПопробуйте еще раз'
        reply_markup = get_ikb_to_menu()
        await answer_message(msg=msg, new_text=new_text, ikb=reply_markup)


def register_add_to_check_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(message_add_to_check, state=AddToCheckStatesGroup.add_to_check,
                                content_types=types.ContentType.TEXT)