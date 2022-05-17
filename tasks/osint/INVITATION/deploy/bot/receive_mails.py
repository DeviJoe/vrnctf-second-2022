import re
import datetime
from datetime import timedelta
from datetime import datetime

from defines import *
import data_sqlite
import email_utils


def write_data_to_sql(mail_id, from_email, topic, content):
    mail_already_in_db = data_sqlite.sql_check_exist(mail_id)
    if not mail_already_in_db:
        data_sqlite.sql_insert_mail(mail_id, from_email, topic, content)


# Проверяем почту через модуль _email2, записываем данные в k
mails = email_utils.check_email_box()

for mail in mails:
    write_data_to_sql(mail[0], mail[1], mail[2], mail[3])
