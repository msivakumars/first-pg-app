import smtplib

from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
pwd = os.getenv("EMAIL_PWD")
me = 'msivakumar1971@hotmail.com'


def send_email(to, sub, body):
    email = EmailMessage()
    email['Subject'] = sub
    email['From'] = me
    email['To'] = to

    email.set_content(body)

    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()

    s.login(me, pwd)

    s.send_message(email)
    s.quit()


def send_user_registration_email(email_id, username):
    return send_email(
        email_id,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores REST API.",
    )