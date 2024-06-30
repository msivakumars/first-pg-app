import smtplib

from email.message import EmailMessage
import os


def send_email(to, sub, body):
    email = EmailMessage()

    me = 'msivakumar1971@hotmail.com'
    email['Subject'] = sub
    email['From'] = me
    email['To'] = to

    email.set_content(body)

    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    pwd= os.getenv("EMAIL_PWD")

    s.login(me, pwd)

    s.send_message(email)
    s.quit()

