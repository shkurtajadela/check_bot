from bot.db.db_interface import get_check, get_conn_by_check
from bot.help_func.help_func import calc_paid_sum
from typing import List
from bot.help_func.bot_func import bot, get_username


def show_created_check_info(description: str, check_sum: str = None, own_sum: str = None, requisites: str = None):
    if not check_sum:
        return f'Описание: {description}'
    elif not own_sum:
        return f'Описание: {description}\nСумма: {check_sum}р'
    elif not requisites:
        return f'Описание: {description}\nСумма: {own_sum}р/{check_sum}р'
    else:
        return f'Описание: {description}\nСумма: {own_sum}р/{check_sum}р\nРеквизиты: {requisites}'
    

def show_check_info(check_sum: int, description: str, requisites: str, username: str):
    return f'Описание: {description}\nСумма: {check_sum}р\nРеквизиты: {requisites}\nВладелец: {username}'


def status_emoji(status: str):
    emoji = {
        '0': '❌',
        '1': '✅'
    }

    return emoji[status]


def sort_conns(conns: List[dict]) -> List[dict]:
    sorted_conns = sorted(conns, key=lambda x: list(map(int, get_check(x['check_id'])['check_date'].split('-')))[::-1],
                          reverse=True)
    return sorted_conns


def sort_checks(checks: List[dict]) -> List[dict]:
    sorted_checks = sorted(checks, key=lambda x: list(map(int, x['check_date'].split('-')))[::-1],
                           reverse=True)
    return sorted_checks


def show_added_checks_info(conns: List[dict]):
    sorted_conns = sort_conns(conns)
    text = ''
    for i, conn in enumerate(sorted_conns):
        check = get_check(conn['check_id'])
        text += f"🧾 Чек №{i+1}, ID: {check['check_id']}\nОписание: {check['description']}\nСумма: {sorted_conns[i]['conn_sum']}р\nДата: {check['check_date']}\nСтатус: {status_emoji(str(sorted_conns[i]['conn_status']))}\n\n"
    return text


def show_my_checks_info(checks: List[dict]):
    sorted_checks= sort_checks(checks)
    text = ''
    for i, check in enumerate(sorted_checks):
        text += f"🧾 Чек №{i+1}, ID: {check['check_id']}\nОписание: {check['description']}\nСумма: {calc_paid_sum(check['check_id'], check['own_sum'])}р/{check['check_sum']}р\nДата: {check['check_date']}\n\n"
    return text


async def show_check_conns_info(conns: List[dict], check_id: str):
    check = get_check(check_id)
    text = f"Описание: {check['description']}\nСумма: {calc_paid_sum(check['check_id'], check['own_sum'])}р/{check['check_sum']}р"
    if len(conns) > 0:
        text += "\n\nДолжники этого чека:\n"
        for j in range(len(conns)):
            username = await get_username(chat_id=conns[j]['user_id'])
            text += f"{username} {status_emoji(str(conns[j]['conn_status']))}"
            if conns[j]['conn_sum']:
                text += f" - {conns[j]['conn_sum']}р"
            text += '\n'
    else:
        text += "\n\nЕще никто не добавился в ваш чек"
    return text