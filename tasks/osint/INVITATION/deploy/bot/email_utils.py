import smtplib
from email.mime.text import MIMEText
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
import mailparser
import email
import imaplib

from defines import *


def check_email_folder(mail, folder):
    mail.select()
    mail.select(folder)
    # it will return with its status and a list of ids
    status, data = mail.search(None, 'ALL')
    # by white spaces on this format: [b'1 2 3', b'4 5 6']
    mail_ids = []
    for block in data:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()
    # now for every id we'll fetch the email
    # to extract its content
    email_list = []
    for i in mail_ids:
        email_ = [f"{i.decode('utf-8')}_{folder}"]
        print(f'{email_}')
        # the fetch function fetch the email given its id
        # and format that you want the message to be
        status, data = mail.fetch(i, '(RFC822)')
        # the content data at the '(RFC822)' format comes on
        # a list with a tuple with header, content, and the closing
        # byte b')'
        for response_part in data:
            # so if its a tuple...
            if isinstance(response_part, tuple):
                # print(response_part[1])
                mail_p = mailparser.parse_from_bytes(response_part[1])
                if len(mail_p.from_[0]) > 1:
                    email_.append(mail_p.from_[0][1])
                else:
                    email_.append(mail_p.from_[0][0])
                # if 'yandex' in email_[len(email_) - 1]:
                #     email_.append(mail_p.subject.encode('latin1', errors='ignore').decode('utf-8'))
                #     email_.append(mail_p.body.encode('latin1', errors='ignore').decode('utf-8'))
                # else:
                email_.append(mail_p.subject)
                email_.append(mail_p.body)
                email_.append('html')
        email_list.append(email_)
    return email_list


# Функция проверки почтовго ящика
def check_email_box():
    # возвращает значения [[id, from, subject, content],[...]]

    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(RECEIVE_MAIL, RECEIVE_PASS)

    email_list = []
    email_list.extend(check_email_folder(mail, 'inbox'))
    email_list.extend(check_email_folder(mail, 'Spam'))

    return email_list


# Отправка почты
def send_email(subject_, message_, to_addrs, format='html'):

    message = MIMEMultipart("alternative")
    if format == 'html':
        message = MIMEMultipart("alternative", None, [MIMEText(message_, 'html', 'utf-8')])
    if format == 'text':
        message = MIMEMultipart("alternative", None, [MIMEText(message_)])
    message['subject'] = subject_
    message['from'] = from_addr
    if to_addrs == list(to_addrs):
        message['to'] = ', '.join(to_addrs)
    else:
        message['to'] = (to_addrs)
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(SEND_MAIL, SEND_PASS)
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()
