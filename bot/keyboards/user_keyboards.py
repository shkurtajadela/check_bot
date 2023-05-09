from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.db.db_interface import *
from bot.help_func.show_func import sort_conns, sort_checks


ikbb_start = InlineKeyboardButton(text='Начать ➡',
                                         callback_data='start')

ikbb_create_check = InlineKeyboardButton(text='Создать чек ✍🏻',
                                         callback_data='create_check')
ikbb_add_to_check = InlineKeyboardButton(text='Добавиться в чек ➕',
                                         callback_data='add_to_check')
ikbb_pay_check= InlineKeyboardButton(text='Оплатить чек 💳',
                                     callback_data='pay_check')
ikbb_my_checks = InlineKeyboardButton(text='Мои чеки 🧾',
                                      callback_data='my_checks')

ikbb_to_menu = InlineKeyboardButton(text='Вернуться в меню ⬅',
                                    callback_data='to_menu')

ikbb_check_submission_yes = InlineKeyboardButton(text='Да, создать чек ✅',
                                                 callback_data='yes')
ikbb_check_submission_no = InlineKeyboardButton(text='Нет, заполнить заново ❌',
                                                callback_data='no')

ikbb_check_payement_yes = InlineKeyboardButton(text='Да, чек оплачен 💳',
                                                 callback_data='yes')
ikbb_check_payement_no = InlineKeyboardButton(text='Нет, чек не оплачен 💤',
                                                callback_data='no')

ikbb_check_delete = InlineKeyboardButton(text='Удалить чек 🗑',
                                                 callback_data='delete_check')
ikbb_pay_check_notification = InlineKeyboardButton(text='Оповестить должников 💤',
                                                callback_data='pay_notification')

ikbb_check_delete_yes = InlineKeyboardButton(text='Да, удалить чек 🗑',
                                                 callback_data='yes')
ikbb_check_delete_no = InlineKeyboardButton(text='Нет, не удалять чек 🧾',
                                                callback_data='no')



def get_ikb_start() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_start)
    return ikb_start


def get_ikb_main() -> InlineKeyboardMarkup:
    ikb_main = InlineKeyboardMarkup(row_width=1)
    ikb_main.add(ikbb_create_check, ikbb_add_to_check, ikbb_pay_check, ikbb_my_checks)
    return ikb_main


def get_ikb_to_menu() -> InlineKeyboardMarkup:
    ikb_to_menu = InlineKeyboardMarkup(row_width=1)
    ikb_to_menu.add(ikbb_to_menu)
    return ikb_to_menu


def get_ikb_check_submission() -> InlineKeyboardMarkup:
    ikb_check_submission = InlineKeyboardMarkup(row_width=1)
    ikb_check_submission.add(ikbb_check_submission_yes, ikbb_check_submission_no)
    return ikb_check_submission


def get_ikb_added_check(conns: List[dict]) -> InlineKeyboardMarkup:
    ikb_added_checks = InlineKeyboardMarkup(row_width=2)
    buttons = []
    sorted_conns = sort_conns(conns)
    for i in range(len(sorted_conns)):
        button_text = f'Чек №{i + 1} '
        if sorted_conns[i]['conn_status']:
            button_text += '✅'
        else:
            button_text += '❌'
        buttons.append(InlineKeyboardButton(text=button_text, callback_data=sorted_conns[i]['check_id']))
        ikb_added_checks = check_len_buttons(buttons=buttons, ikbb=ikb_added_checks, end=0)
        if len(buttons) == 2: 
            buttons = []
    ikb_added_checks = check_len_buttons(buttons=buttons, ikbb=ikb_added_checks, end=1)
    ikb_added_checks.add(ikbb_to_menu)
    return ikb_added_checks


def check_len_buttons(buttons: List[InlineKeyboardButton], ikbb: InlineKeyboardMarkup, end: int):
    if len(buttons) == 2 and end == 0:
        ikbb.add(buttons[0], buttons[1])
    if len(buttons) == 1 and end == 1:
        ikbb.add(buttons[0])
    return ikbb


def get_ikb_check_payement() -> InlineKeyboardMarkup:
    ikb_check_payement = InlineKeyboardMarkup(row_width=1)
    ikb_check_payement.add(ikbb_check_payement_yes, ikbb_check_payement_no)
    return ikb_check_payement


def get_ikb_my_checks(checks: List[dict]) -> InlineKeyboardMarkup:
    ikb_check_ids = InlineKeyboardMarkup(row_width=2)
    buttons = []
    sorted_checks = sort_checks(checks)
    for i in range(len(sorted_checks)):
        button = InlineKeyboardButton(text=f'Чек №{i + 1} 🧾', callback_data=sorted_checks[i]['check_id'])
        buttons.append(button)
        ikb_check_ids = check_len_buttons(buttons=buttons, ikbb=ikb_check_ids, end=0)
        if len(buttons) == 2: 
            buttons = []    
    ikb_check_ids = check_len_buttons(buttons=buttons, ikbb=ikb_check_ids, end=1)
    ikb_check_ids.add(ikbb_to_menu)
    return ikb_check_ids


def get_ikb_check_delete() -> InlineKeyboardMarkup:
    ikb_check_delete = InlineKeyboardMarkup(row_width=1)
    ikb_check_delete.add(ikbb_check_delete_yes, ikbb_check_delete_no)
    return ikb_check_delete


def get_ikb_check_info() -> InlineKeyboardMarkup:
    ikb_check_info = InlineKeyboardMarkup(row_width=1)
    ikb_check_info.add(ikbb_check_delete, ikbb_pay_check_notification, ikbb_to_menu)
    return ikb_check_info


def get_ikb_notification(check_id) -> InlineKeyboardMarkup:
    ikbb_to_check = InlineKeyboardButton(text='Перейти к оплате ➡', callback_data=f'notification:{check_id}')
    ikb_notification = InlineKeyboardMarkup(row_width=1)
    ikb_notification.add(ikbb_to_check)
    return ikb_notification
