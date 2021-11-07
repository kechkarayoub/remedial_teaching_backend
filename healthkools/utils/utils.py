# -*- coding: utf-8 -*-

import datetime
from django.core.mail import send_mail
from django.conf import settings
import after_response
import base64
import requests


def date_from_string(date_string):
    try:
        return datetime.datetime.strptime(date_string, "%d/%m/%Y")
    except:
        return None


@after_response.enable
def send_email(subject, message_txt, list_emails, html_message=None):
    if settings.EMAIL_SMTP_PROVIDER == "sendgrid":
        send_mail(subject, message_txt, 'edxkls2019@gmail.com', list_emails, html_message=html_message)


def get_static_logo_url():
    return settings.BACKEND_URL + "/static/images/logo.jpg"


def get_img_as_base64(url):
    return base64.b64encode(requests.get(url).content).decode('ascii')

