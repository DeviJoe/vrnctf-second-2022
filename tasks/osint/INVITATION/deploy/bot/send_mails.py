import re
import datetime
from datetime import timedelta
from datetime import datetime

from defines import *
import data_sqlite
import email_utils
import parse_mail


mails = data_sqlite.sql_row_names()

for mail in mails:
    mail_id = mail[1]
    send_to = mail[3]
    topic = mail[4]
    content = mail[5]

    if data_sqlite.sql_check_status(mail_id):
        continue

    ret = parse_mail.parse_mail(topic, content)
    if ret:
        email_utils.send_email(f'RE: {topic}', ret, send_to)
        data_sqlite.sql_update_mail_status(mail_id, True)
    else:
        data_sqlite.sql_update_mail_status(mail_id, True)

