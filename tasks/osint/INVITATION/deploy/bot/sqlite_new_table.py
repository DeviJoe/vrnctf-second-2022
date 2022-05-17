import sqlite3

from defines import *

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

# Создание таблицы
cursor.execute(
    """
    CREATE TABLE test_db (
        id integer primary key, 
        mail_id text, 
        status integer, 
        from_email text, 
        topic text, 
        content text
    )
    """
)
