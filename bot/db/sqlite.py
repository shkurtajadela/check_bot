import sqlite3 as sq


def db_start():
    global db, cur

    db = sq.connect('bot_db.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Checks(check_id TEXT PRIMARY KEY, owner_id INTEGER, photo TEXT, "
                "check_sum INTEGER, own_sum INTEGER, description TEXT, requisites TEXT, check_date TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Connections(conn_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,"
                " check_id TEXT, conn_sum INTEGER, conn_status INTEGER,"
                " FOREIGN KEY (check_id) REFERENCES Checks(check_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS Users(user_id INTEGER PRIMARY KEY, chat_id INTEGER,"
                " msg_id INTEGER)")
    db.commit()


def new_check(check_id: str, owner_id: int, photo: str, check_sum: int, own_sum: int,
              description: str, requisites: str, check_date: str):
    cur.execute("INSERT INTO Checks VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                (check_id, owner_id, photo, check_sum, own_sum, description, requisites, check_date))

    db.commit()


def new_check_empty(check_id: str, owner_id: int, description: str, requisites: str, check_date: str):
    cur.execute("INSERT INTO Checks VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                (check_id, owner_id, '', '', '', description, requisites, check_date))

    db.commit()


def update_photo(check_id: str, photo: str):
    cur.execute(f"UPDATE Checks SET photo = '{photo}' WHERE check_id == '{check_id}'")
    db.commit()


def update_own_sum(check_id: str, own_sum: int):
    cur.execute(f"UPDATE Checks SET own_sum = {own_sum} WHERE check_id == '{check_id}'")
    db.commit()


def update_check_sum(check_id: str, check_sum: int):
    cur.execute(f"UPDATE Checks SET check_sum = {check_sum} WHERE check_id == '{check_id}'")
    db.commit()


def update_description(check_id: str, description: str):
    cur.execute(f"UPDATE Checks SET description = '{description}' WHERE check_id == '{check_id}'")
    db.commit()


def update_requisites(check_id: str, requisites: str):
    cur.execute(f"UPDATE Checks SET requisites = '{requisites}' WHERE check_id == '{check_id}'")
    db.commit()


def delete_check(check_id: str):
    cur.execute(f"DELETE FROM Checks WHERE check_id == '{check_id}'")
    db.commit()


def get_checks_by_user(owner_id: int):
    value = cur.execute(f"SELECT * FROM Checks WHERE owner_id == {owner_id}").fetchall()
    return value


def get_check(check_id: str):
    value = cur.execute(f"SELECT * FROM Checks WHERE check_id == '{check_id}'").fetchone()
    return value


def new_conn(user_id: int, check_id: str):
    cur.execute("INSERT INTO Connections VALUES(?, ?, ?, ?, ?)",
                (None, user_id, check_id, 0, 0))

    db.commit()


def update_conn_sum(conn_id: int, conn_sum: int):
    cur.execute(f"UPDATE Connections SET conn_sum = {conn_sum} WHERE conn_id == {conn_id}")
    db.commit()


def update_conn_status(conn_id: int, conn_status: int):
    cur.execute(f"UPDATE Connections SET conn_status = {conn_status} WHERE conn_id == {conn_id}")
    db.commit()


def delete_conns(check_id: str):
    cur.execute(f"DELETE FROM Connections WHERE check_id == '{check_id}'")
    db.commit()


def get_conns_by_check(check_id: str):
    value = cur.execute(f"SELECT * FROM Connections WHERE check_id == '{check_id}'").fetchall()
    return value


def get_conns_by_user(user_id: int):
    value = cur.execute(f"SELECT * FROM Connections WHERE user_id == {user_id}").fetchall()
    return value


def get_conn_by_user_and_check(user_id: int, check_id: str):
    value = cur.execute(f"SELECT * FROM Connections WHERE user_id == {user_id} AND check_id == '{check_id}'").fetchone()
    return value


def new_user(user_id: int, chat_id: int, msg_id: int):
    cur.execute("INSERT INTO Users VALUES(?, ?, ?)",
                (user_id, chat_id, msg_id))
    db.commit()


def get_msg_id(user_id: int):
    value = cur.execute(f"SELECT * FROM Users WHERE user_id == {user_id}").fetchone()
    return value


def update_user(user_id: int, chat_id: int, msg_id: int):
    cur.execute(f"UPDATE Users SET chat_id = {chat_id}, msg_id = {msg_id} WHERE user_id == {user_id}")
    db.commit()


def get_user_by_chat(chat_id: int):
    value = cur.execute(f"SELECT * FROM Users WHERE chat_id == {chat_id}").fetchone()
    return value
