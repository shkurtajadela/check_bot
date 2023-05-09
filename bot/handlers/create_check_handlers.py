from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.keyboards.user_keyboards import *
from bot.states_groups.states_groups import *
from bot.db.db_interface import *
from bot.help_func.show_func import show_created_check_info
from bot.handlers.edit_message_func import answer_message, answer_callback
from bot.handlers.main_handlers import callback_or_message_start


async def message_load_check_photo(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = msg.photo[0].file_id
        data['user_id'] = msg.from_user.id

        new_text = 'Напишите описание чека'
        reply_markup = get_ikb_to_menu()
        await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])
        await CheckCreationStatesGroup.next()


async def message_load_check_description(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = msg.text

        new_text = show_created_check_info(description=data['description']) \
                   + '\n\nВведите общую сумму чека (в рублях)'
        reply_markup = get_ikb_to_menu()
        await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])
        await CheckCreationStatesGroup.next()


async def message_load_check_summ(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if not msg.text.isdigit():
            new_text = show_created_check_info(description=data['description']) + \
                       '\n\nСумма должна быть числом\n\nВведите общую сумму чека (в рублях)'
            reply_markup = get_ikb_to_menu()
            await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])
        else:
            data['check_sum'] = msg.text

            new_text = show_created_check_info(description=data['description'],check_sum=data['check_sum']) \
                       + '\n\nВведите сумму своего заказа (в рублях)'
            reply_markup = get_ikb_to_menu()
            await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])
            await CheckCreationStatesGroup.next()


async def message_load_check_summ_own(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if not msg.text.isdigit():
            new_text = show_created_check_info(description=data['description'],check_sum=data['check_sum']) +\
                       '\n\nСумма должна быть числом\n\nВведите сумму своего заказа (в рублях)'
            reply_markup = get_ikb_to_menu()
            await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])
        elif int(msg.text) >= int(data['check_sum']):
            new_text = show_created_check_info(description=data['description'],check_sum=data['check_sum']) + \
                       '\n\nСумма заказа должна быть меньше общей суммы чека\n\nВведите сумму своего заказа (в рублях)'
            reply_markup = get_ikb_to_menu()
            await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])
        else:
            data['own_sum'] = msg.text

            new_text = show_created_check_info(description=data['description'],
                                               check_sum=data['check_sum'],
                                               own_sum=data['own_sum']) + '\n\nНапишите свои реквизиты'
            reply_markup = get_ikb_to_menu()
            await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])
            await CheckCreationStatesGroup.next()


async def message_load_check_requisites(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['requisites'] = msg.text
        new_text = show_created_check_info(check_sum=data['check_sum'],
                                           own_sum=data['own_sum'],
                                           description=data['description'],
                                           requisites=data['requisites']) + '\n\nВсе верно?'
        reply_markup = get_ikb_check_submission()
        await answer_message(msg=msg, new_text=new_text, ikb=reply_markup, photo=data['photo'])
        await CheckSubmissionStatesGroup.check_submission.set()


async def callback_check_submission(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        async with state.proxy() as data:
            check_id = new_check(owner_id=data['user_id'],
                                 photo=data['photo'],
                                 check_sum=data['check_sum'],
                                 own_sum=data['own_sum'],
                                 description=data['description'],
                                 requisites=data['requisites'])
        text = 'Чек успешно создан. ID: ' + check_id
        await callback_or_message_start(callback=callback, text=text)
    elif callback.data == 'no':
        new_text = 'Пришлите фотографию чека'
        reply_markup = get_ikb_to_menu()
        await answer_callback(callback=callback, new_text=new_text, ikb=reply_markup)
        await CheckCreationStatesGroup.photo.set()
    await callback.answer()


def register_create_check_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(message_load_check_photo, state=CheckCreationStatesGroup.photo,
                                content_types=types.ContentType.PHOTO)
    dp.register_message_handler(message_load_check_description, state=CheckCreationStatesGroup.description,
                                content_types=types.ContentType.TEXT)
    dp.register_message_handler(message_load_check_summ, state=CheckCreationStatesGroup.summ,
                                content_types=types.ContentType.TEXT)
    dp.register_message_handler(message_load_check_summ_own, state=CheckCreationStatesGroup.summ_own,
                                content_types=types.ContentType.TEXT)
    dp.register_message_handler(message_load_check_requisites, state=CheckCreationStatesGroup.requisites,
                                content_types=types.ContentType.TEXT)
    dp.register_callback_query_handler(callback_check_submission, state=CheckSubmissionStatesGroup.check_submission)
