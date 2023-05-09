from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.db.db_interface import is_check_in_db
from bot.handlers.pay_check_handlers import callback_load_check_sum
from bot.handlers.main_handlers import callback_or_message_start
from bot.states_groups.states_groups import PayCheckStatesGroup
from bot.help_func.bot_func import bot


async def callback_open_notification(callback: types.CallbackQuery, state: FSMContext):
    check_id = callback.data.split(':')[1]
    if not is_check_in_db(check_id):
        text = 'Этот чек был удален владельцем'
        await callback_or_message_start(callback=callback, text=text)
    else:
        await PayCheckStatesGroup.pay_check.set()
        await callback_load_check_sum(callback=callback, state=state)


def register_notification_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(callback_open_notification, lambda x: x.data.split(':')[0] == 'notification', state='*')
    # dp.register_callback_query_handler(callback_open_notification, lambda x: 'notification' in x.data, state='*')
