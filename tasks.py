import smtplib
import os
from app import celery
import time


@celery.task()
def send_mail(emails):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(os.environ.get('SMTP_LOGIN'),
                  os.environ.get('SMTP_PASSWORD'))
    smtpObj.sendmail(os.environ.get('SMTP_LOGIN'),
                     emails,
                     'Some message')
    time.sleep(1)
    return 'Done'

