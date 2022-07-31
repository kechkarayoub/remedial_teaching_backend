# -*- coding: utf-8 -*-

from .models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import activate, gettext_lazy as _
from utils.utils import send_email, get_img_as_base64, get_static_logo_url
import after_response
import html2text
import logging

logger = logging.getLogger(__name__)


@after_response.enable
def contact_new_user(user, user_email_confirmation_key):
    """
        :param user_email_confirmation_key: the user email confirmation key
        :param user: the new user which will receive an email of confirmation
        :return: None
    """
    # if user.username=="testuser2": import pdb;pdb.set_trace()
    activate(user.language)
    email_subject = _("Your account {site_name}").format(site_name=settings.SITE_NAME)
    context = {
        "direction": "rtl" if user.language == "ar" else "ltr",
        "full_name": user.last_name + " " + user.first_name,
        "logo_url": get_static_logo_url(),
        "site_name": settings.SITE_NAME,
        "site_url": settings.FRONT_URL,
        "subject": email_subject,
        "validation_url": settings.FRONT_URL + "/validation_email/" + user_email_confirmation_key,
    }
    email_message_txt = render_to_string('emails/confirmation_email.txt', context)
    email_message_html = render_to_string('emails/confirmation_email.html', context)
    # email_message_txt_html = email_message_html.split('main>')[1][:-2].replace("<b>", "").replace("</b>", "")
    # email_message_txt = html2text.html2text(email_message_txt_html)
    """
        For localhost; execute this code in navigator server to show images in email client:
            var images = document.querySelectorAll("img");
            for(var i=0; i<images.length; i++) {
                console.log(images[i].src);
                images[i].src=images[i].src.replace(/^https:\/\/[a-zA-Z0-9.\/\-=_]+#/,'');
            }
    """
    response = send_email(email_subject, email_message_txt, [user.email], html_message=email_message_html)
    if response == "no_smtp_email_provider":
        logger.warning('You should configure a smtp email provider')


def get_user_by_email_or_username(email_or_username):
    """
        :param email_or_username: a string contains the email or username
        :return: return the user linked to the username or email if exists else "not_exists" if not exists else None
    """
    try:
        if "@" in email_or_username:
            user = User.objects.get(email=email_or_username)
        else:
            user = User.objects.get(username=email_or_username)
        return user
    except User.DoesNotExist:
        return "not_exists"
    except:
        return None
