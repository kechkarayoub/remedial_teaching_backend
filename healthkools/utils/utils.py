# -*- coding: utf-8 -*-

import datetime
from django.core.mail import send_mail
from django.conf import settings
import after_response
import base64
import requests


def date_from_string(date_string):
    """
        :param date_string: date string from the user request
        :return: return a date object if the string match "%d/%m/%Y" format else return None
    """
    try:
        return datetime.datetime.strptime(date_string, "%d/%m/%Y")
    except:
        return None


@after_response.enable
def send_email(subject, message_txt, list_emails, html_message=None):
    """
        :param subject: subject of the email
        :param message_txt: plain text of the email
        :param list_emails: list of receivers addresses of the of the email
        :param html_message: html_message of the email
        :return: None
    """
    if settings.EMAIL_SMTP_PROVIDER == "sendgrid":
        return send_mail(subject, message_txt, settings.EMAIL_FROM_ADDRESS, list_emails, html_message=html_message)
    else:
        return "no_smtp_email_provider"


def get_static_logo_url():
    """
        :return: the url of the website logo
    """
    return settings.BACKEND_URL + "/static/images/logo.jpg"


def get_img_as_base64(url):
    """
        :param url: image url
        :return: convert the image url to base64 encode
    """
    return base64.b64encode(requests.get(url).content).decode('ascii')

