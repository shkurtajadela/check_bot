from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.keyboards.user_keyboards import *
from bot.states_groups.states_groups import *
from bot.db.db_interface import *
from bot.handlers.edit_message_func import answer_message, answer_callback
from bot.help_func.show_func import *
from bot.handlers.main_handlers import callback_or_message_start


async def callback_load_choose_check(callback: types.CallbackQuery, state: FSMContext):
    if callback.data != 'to_menu':
        check = get_check(callback.data)
        async with state.proxy() as data:
            data['check_id'] = callback.data
            new_text = await show_check_conns_info(get_conn_by_check(check['check_id']), check['check_id'])
            reply_markup = get_ikb_check_info()
            await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup, photo=check['photo'])
            await InfoCheckStatesGroup.next()

    else:
        await callback_or_message_start(callback=callback)


async def callback_check_info(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.data == 'delete_check':
            new_text = f"Вы действительно хотите удалить чек?"
            reply_markup = get_ikb_check_delete()
            await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup)
            await InfoCheckStatesGroup.next()

        elif callback.data == 'pay_notification':
            conns = get_conn_by_check(data['check_id'])
            blocked_users = []
            payers_cnt = 0
            for conn in conns:
                if conn['conn_status'] == 0:
                    try:
                        await send_notification(conn['user_id'], conn['check_id'])
                        payers_cnt += 1

                    except Exception:
                        username = await get_username(conn['user_id'])
                        blocked_users.append(username)

            if blocked_users:
                if len(conns) == len(blocked_users):
                    text = 'Не удалось оповестить должников'

                else:
                    text = 'Оповещены все должники, кроме:\n'

                    for user in blocked_users:
                        text += f'\n{user}'

            elif payers_cnt == 0:
                text = 'Должников нет'

            else:
                text = 'Должники оповещены успешно'
            await callback_or_message_start(callback=callback, text=text)

        else:
            await callback_or_message_start(callback=callback)
    await callback.answer()


async def send_notification(user_id, check_id):
    message = f"Привет! Чек (ID: {check_id}) ждет оплату\n\nНажмите на кнопку ниже, чтобы прочитать инфорамцию о чеке и потом его оплатить "
    reply_markup = get_ikb_notification(check_id=check_id)
    await bot.delete_message(chat_id=user_id, message_id=get_user(user_id)['msg_id'])
    new_msg = await bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)
    new_user(user_id=user_id, chat_id=get_user(user_id)['chat_id'], msg_id=new_msg.message_id)


async def callback_check_submission(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        async with state.proxy() as data:
            delete_check(data['check_id'])
            text = 'Чек был успешно удален'
            await callback_or_message_start(callback=callback, text=text)
    elif callback.data == 'no':
        await callback_or_message_start(callback=callback)
    await callback.answer()


def register_my_checks_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(callback_load_choose_check, state=InfoCheckStatesGroup.choose_check)
    dp.register_callback_query_handler(callback_check_info, state=InfoCheckStatesGroup.delete_notify_check)
    dp.register_callback_query_handler(callback_check_submission, state=InfoCheckStatesGroup.delete_confirm)
