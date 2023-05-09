from aiogram import types, Dispatcher

from bot.keyboards.user_keyboards import *
from bot.states_groups.states_groups import *
from bot.db.db_interface import *
from bot.help_func.bot_func import bot, logo_photo
from bot.handlers.edit_message_func import answer_message, answer_callback
from bot.help_func.show_func import show_my_checks_info, show_added_checks_info


async def cmd_start(msg: types.Message) -> None:
    photo = logo_photo
    new_text = 'Привет, я ДелиЧек - бот для дележки чека!'
    reply_markup = get_ikb_start()
    if is_user(msg.from_user.id):
        await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=photo)
        await StartStatesGroup.start.set()

    else:
        new_msg = await msg.answer_photo(photo=photo,caption=new_text, reply_markup=reply_markup)
        new_user(user_id=msg.from_user.id, chat_id=new_msg.chat.id, msg_id=new_msg.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        await StartStatesGroup.start.set()


async def callback_or_message_start(callback: types.CallbackQuery = None, msg: types.Message = None, text: str = None) -> None:
    photo = logo_photo
    new_text = ''
    if text:
        new_text += text + '\n\n'
    new_text += 'Что вы хотите сделать?'
    reply_markup = get_ikb_main()

    if callback:
        await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup, photo=photo)
    elif msg:
        await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=photo)
    await MainMenuStatesGroup.main_menu.set()


async def callback_to_menu(callback: types.CallbackQuery):
    if callback.data == 'to_menu':
        await callback_or_message_start(callback)


async def callback_main_menu(callback: types.CallbackQuery):
    if callback.data == 'create_check':
        new_text = 'Пришлите фотографию чека'
        reply_markup = get_ikb_to_menu()
        await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup)
        await CheckCreationStatesGroup.photo.set()
    elif callback.data == 'add_to_check':
        new_text = 'Напишите ID чека'
        reply_markup = get_ikb_to_menu()
        await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup)
        await AddToCheckStatesGroup.add_to_check.set()
    elif callback.data == 'pay_check':
        conns = get_conn_by_user(callback.from_user.id)
        reply_markup = get_ikb_added_check(conns)
        if len(conns) > 0:
            new_text = 'Список добавленных чеков:\n\n' + show_added_checks_info(conns)
            await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup)
            await PayCheckStatesGroup.pay_check.set()
        else:
            new_text = 'Нет добавленных чеков'
            await callback_or_message_start(callback=callback, text=new_text)
    elif callback.data == 'my_checks':
        checks = get_checks(callback.from_user.id)
        reply_markup = get_ikb_my_checks(checks)
        if len(checks) > 0:
            new_text = 'Список созданных чеков:\n\n' + show_my_checks_info(checks)
            await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup)
            await InfoCheckStatesGroup.choose_check.set()
        else:
            new_text = 'Нет созданных чеков'  
            await callback_or_message_start(callback=callback, text=new_text)
    await callback.answer()


async def cmd_help(msg: types.Message) -> None:
    photo = logo_photo
    new_text = 'Список команд бота ДелиЧек:\n\n' \
               '/start - Запустить бота\n' \
               '/help - Открыть список команд\n' \
               '/description - Открыть описание бота'
    reply_markup = get_ikb_start()
    await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=photo)
    await StartStatesGroup.start.set()


async def cmd_description(msg: types.Message) -> None:
    photo = logo_photo
    new_text = 'Привет, я ДелиЧек - бот для дележки чека!'
    reply_markup = get_ikb_start()
    await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=photo)
    await StartStatesGroup.start.set()


def register_commands(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands=['start'], state='*')

    dp.register_message_handler(cmd_help, commands=['help'], state='*')

    dp.register_message_handler(cmd_description, commands=['description'], state='*')


def register_main_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(callback_or_message_start, state=StartStatesGroup.start)

    dp.register_callback_query_handler(callback_main_menu, state=MainMenuStatesGroup.main_menu)

    dp.register_callback_query_handler(callback_to_menu, state='*')