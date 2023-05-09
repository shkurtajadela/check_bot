def parse_check(db_check: tuple):
    check = {
        'check_id': db_check[0],
        'owner_id': db_check[1],
        'photo': db_check[2],
        'check_sum': db_check[3],
        'own_sum': db_check[4],
        'description': db_check[5],
        'requisites': db_check[6],
        'check_date': db_check[7],
    }

    return check


def parse_user(db_user: tuple):
    user = {
        'user_id': db_user[0],
        'chat_id': db_user[1],
        'msg_id': db_user[2],
    }

    return user


def parse_checks(db_checks: list):
    checks = [parse_check(db_check=db_check) for db_check in db_checks]

    return checks


def parse_conn(db_conn: tuple):
    conn = {
        'conn_id': db_conn[0],
        'user_id': db_conn[1],
        'check_id': db_conn[2],
        'conn_sum': db_conn[3],
        'conn_status': db_conn[4],
    }

    return conn


def parse_conns(db_conns: list):
    conns = [parse_conn(db_conn=db_conn) for db_conn in db_conns]

    return conns
