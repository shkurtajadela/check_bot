from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.keyboards.user_keyboards import *
from bot.states_groups.states_groups import *
from bot.db.db_interface import *
from bot.handlers.main_handlers import callback_or_message_start
from bot.handlers.edit_message_func import answer_message, answer_callback
from bot.help_func.show_func import show_check_info
from bot.help_func.bot_func import get_username


async def callback_load_check_sum(callback: types.CallbackQuery, state: FSMContext):
    if callback.data != 'to_menu':
        try:
            if 'notification' in callback.data:
                callback_data = callback.data.split(':')[1]
            else:
                callback_data = callback.data
            check = get_check(callback_data)
            async with state.proxy() as data:
                data['conn_id'] = get_conn_by_user_and_check(callback.from_user.id, callback_data)['conn_id']
                data['photo'] = check['photo']
                data['check_sum'] = check['check_sum']
                data['own_sum'] = check['own_sum']
                data['description'] = check['description']
                data['requisites'] = check['requisites']
                data['username'] = await get_username(check['owner_id'])
                data['status'] = get_conn_by_user_and_check(callback.from_user.id, callback_data)['conn_status']
                new_text = show_check_info(check_sum=check['check_sum'],
                                            description=check['description'],
                                            requisites=check['requisites'],
                                            username=data['username'])
                if data['status'] != 0:
                    new_text += '\n\nHапишите вашу новую сумму (в рублях)'
                else:
                    new_text += '\n\nHапишите вашу сумму (в рублях)'
                reply_markup = get_ikb_to_menu()
                await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup, photo=check['photo'])
                await PayCheckStatesGroup.next()

        except TypeError:
            text = 'Этот чек был удален владельцем'
            await callback_or_message_start(callback=callback, text=text)

    else:
        await callback_or_message_start(callback=callback)


async def message_load_check_requisites(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if not msg.text.isdigit():
            new_text = show_check_info(check_sum=data['check_sum'],
                                       description=data['description'],
                                       requisites=data['requisites'],
                                       username=data['username'])
            new_text += "\n\nСумма должна быть числом\n\nВведи сумму своего заказа (в рублях)"
            reply_markup = get_ikb_to_menu()
            await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])

        elif int(msg.text) >= int(data['check_sum']) - int(data['own_sum']):
            new_text = show_check_info(check_sum=data['check_sum'],
                                       description=data['description'],
                                       requisites=data['requisites'],
                                       username=data['username'])
            new_text += "\n\nСумма заказа должна быть меньше общей суммы чека\n\nВведи сумму своего заказа (в рублях)"
            reply_markup = get_ikb_to_menu()
            await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])

        else:
            data['conn_sum'] = msg.text
            new_text = f"Реквизиты: {data['requisites']}\n\nПереведите сумму {data['conn_sum']}р"
            reply_markup = get_ikb_check_payement()
            await answer_message(msg=msg, new_text=new_text, ikb=reply_markup)
            await PayCheckStatesGroup.next()


async def callback_payement_check(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.data == 'yes':
            if data['status'] == 1:
                text = 'Информация об новой оплате добавлена'
            else:
                text = 'Информация об оплате добавлена'
            update_conn(conn_id=data['conn_id'], conn_sum=data['conn_sum'])
            update_conn(conn_id=data['conn_id'], conn_status=1)
            await callback_or_message_start(callback=callback, text=text)
        elif callback.data == 'no':
            await callback_or_message_start(callback=callback)
    await callback.answer()


def register_pay_check_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(callback_load_check_sum, state=PayCheckStatesGroup.pay_check)
    dp.register_message_handler(message_load_check_requisites, state=PayCheckStatesGroup.summ_to_pay)
    dp.register_callback_query_handler(callback_payement_check, state=PayCheckStatesGroup.summ_paid)
