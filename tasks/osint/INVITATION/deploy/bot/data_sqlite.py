import sqlite3

from defines import *


def sql_insert_mail(mail_id, from_email, topic, content):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO {TABLE_NAME} VALUES (NULL, ?, FALSE, ?, ?, ?)',
                   (mail_id, from_email, topic, content))
    conn.commit()
    conn.close()


def sql_delete_mail(mail_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {TABLE_NAME} WHERE mail_id == ?', [mail_id])
    conn.commit()
    conn.close()


def sql_update_mail_status(mail_id, status):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # cursor.execute("UPDATE " + TABLE_NAME + " SET " + data)
    cursor.execute(f'UPDATE {TABLE_NAME} SET status == ? WHERE mail_id == ?', (status, mail_id))
    conn.commit()
    conn.close()


def sql_get_posts():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    with conn:
        # cursor.execute("SELECT * FROM " + TABLE_NAME)
        cursor.execute(f'SELECT * FROM {TABLE_NAME}')
        print(cursor.fetchall())


def sql_row_names():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {TABLE_NAME}')
    # names = [description[0] for description in cursor.description]
    names = cursor.fetchall()
    return names


# def sql_select_data(column_, name_):
#     conn = sqlite3.connect(DATABASE_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM " + TABLE_NAME)
#     names = [description[0] for description in cursor.description]
#     cursor.execute("SELECT * FROM " + TABLE_NAME + " WHERE " + column_ + "='" + name_ + "';")
#     rows = cursor.fetchall()
#     for row in rows:
#         names.append(row)
#     conn.commit()
#     conn.close()
#     return names


def sql_check_exist(_id: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'SELECT rowid FROM {TABLE_NAME} WHERE mail_id == ?', [_id])
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True


def sql_check_status(mail_id: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'SELECT rowid FROM {TABLE_NAME} WHERE mail_id == ? and status == TRUE', [mail_id])
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True
