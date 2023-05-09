from bot.db import sqlite
from bot.help_func.help_func import get_date, create_check_id
from bot.help_func.parse_db import parse_check, parse_user, parse_checks, parse_conn, parse_conns


def is_check_in_db(check_id: str):
    if sqlite.get_check(check_id=check_id):
        return True
    return False


def unique_check_id():
    check_id = create_check_id()
    while is_check_in_db(check_id=check_id):
        check_id = create_check_id()

    return check_id


def new_check(owner_id: int, photo: str, check_sum: int, own_sum: int, description: str, requisites: str):
    check_date = get_date()
    check_id = unique_check_id()

    sqlite.new_check(check_id=check_id, owner_id=owner_id, photo=photo, check_sum=check_sum,
                     own_sum=own_sum, description=description, requisites=requisites, check_date=check_date)

    return check_id


def new_check_empty(owner_id: str, description: str, requisites: str):
    check_date = get_date()
    check_id = unique_check_id()

    sqlite.new_check(check_id=check_id, owner_id=owner_id, description=description,
                     requisites=requisites, check_date=check_date)

    return check_id


def get_check(check_id: str):
    db_check = sqlite.get_check(check_id=check_id)
    check = parse_check(db_check=db_check)

    return check


def new_user(user_id: int, chat_id: int, msg_id: int):
    if not is_user(user_id=user_id):
        sqlite.new_user(user_id=user_id, chat_id=chat_id, msg_id=msg_id)
    else:
        sqlite.update_user(user_id=user_id, chat_id=chat_id, msg_id=msg_id)


def is_user(user_id: int):
    user = sqlite.get_msg_id(user_id=user_id)
    if user:
        return True
    return False


def get_user(user_id: int):
    db_user = sqlite.get_msg_id(user_id=user_id)
    user = parse_user(db_user=db_user)

    return user


def get_user_by_chat_id(chat_id):
    db_user = sqlite.get_user_by_chat(chat_id=chat_id)
    user = parse_user(db_user=db_user)

    return user['user_id']


def new_conn(user_id: int, check_id: str):
    sqlite.new_conn(user_id=user_id, check_id=check_id)


def get_checks(owner_id: int):
    db_checks = sqlite.get_checks_by_user(owner_id=owner_id)
    checks = parse_checks(db_checks=db_checks)

    return checks


def is_check_owner(user_id: int, check_id: str):
    check = get_check(check_id=check_id)

    if user_id == check["owner_id"]:
        return True

    return False


def is_conn_in_db(user_id: int, check_id: str):
    if sqlite.get_conn_by_user_and_check(user_id=user_id, check_id=check_id):
        return True

    return False


def get_conn_by_user_and_check(user_id: int, check_id: str):
    db_conn = sqlite.get_conn_by_user_and_check(user_id=user_id, check_id=check_id)
    conn = parse_conn(db_conn=db_conn)

    return conn


def get_conn_by_user(user_id: int):
    db_conns = sqlite.get_conns_by_user(user_id=user_id)
    conns = parse_conns(db_conns=db_conns)

    return conns


def get_conn_by_check(check_id: str):
    db_conns = sqlite.get_conns_by_check(check_id=check_id)
    conns = parse_conns(db_conns=db_conns)

    return conns


def delete_check(check_id: str):
    sqlite.delete_check(check_id=check_id)
    sqlite.delete_conns(check_id=check_id)


def update_conn(conn_id: int, conn_sum: int = None, conn_status: int = None):
    if conn_sum:
        sqlite.update_conn_sum(conn_id=conn_id, conn_sum=conn_sum)
    if conn_status:
        sqlite.update_conn_status(conn_id=conn_id, conn_status=conn_status)