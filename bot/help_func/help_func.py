from datetime import datetime
import secrets
from bot.db.sqlite import get_conns_by_check


def get_date():
    current_date = datetime.now()
    day = current_date.day
    day = str(day).rjust(2, '0')
    month = current_date.month
    month = str(month).rjust(2, '0')
    year = current_date.year
    date = f"{day}-{month}-{year}"

    return date


def create_check_id():
    check_id = secrets.token_hex(nbytes=3)
    return check_id


def calc_paid_sum(check_id: str, own_sum: int):
    all_sum = own_sum
    for conn in get_conns_by_check(check_id):
        all_sum += conn[3]
    return all_sum


