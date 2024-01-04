# -*- coding: utf-8 -*-
import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from colorfield.fields import ColorField
from utils.utils import get_random_bg_color


class User(AbstractUser):
    """
        User represent the user model.
        :attribute: address: CharField represent the address of users
        :attribute: birthday: DateField represent the birthday of users
        :attribute: country_code: CharField represent the country code of users
        :attribute: country_name: CharField represent the country name of users
        :attribute: created_at: DatetimeField represent the time of object creation
        :attribute: created_by: ForeignKey represent the creator of the user.
        :attribute: email_is_validated: BooleanField represent if the users email is validated or not
        :attribute: gender: CharField represent the gender of users
        :attribute: image_url: CharField represent the image of user
        :attribute: initials_bg_color: CharField represent the background color of user's initials
        :attribute: is_deleted: BooleanField represent if the item is deleted by user or not
        :attribute: language: CharField represent the language of users
        :attribute: last_update_at: DatetimeField represent the last time the object updated
        :attribute: last_update_by: ForeignKey represent the last updater of the object.
        :attribute: mobile_phone: CharField represent the mobile_phone of user
        :attribute: mobile_phone_is_valid: BooleanField represent user mobile_phone is valid or not
        :attribute: mobile_phone_is_validated: BooleanField represent user mobile_phone is validated or not
    """
    class Meta(object):
        db_table = "remedial_teaching_user"
        ordering = ["username"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    GENDERS = (
        ("", _("Select")),
        ("f", _("Female")),
        ("m", _("Male")),
    )
    address = models.TextField(_('Address'), default="")
    birthday = models.DateField(_('Birthday'), null=True)
    cin = models.CharField(_('CIN'), blank=False, max_length=15, null=False, unique=True)
    country_code = models.CharField(_('Country code'), blank=True, default="", max_length=10)
    country_name = models.CharField(_('Country name'), blank=True, default="", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey('User', related_name='created_users', on_delete=models.SET_NULL, null=True)
    email_is_validated = models.BooleanField(_('Email is validated'), db_index=True, default=False)
    gender = models.CharField(_('Gender'), blank=True, choices=GENDERS, default="", max_length=10)
    image_url = models.CharField(_('Image url'), blank=True, default="", max_length=512)
    initials_bg_color = ColorField(_('Initials background color'), default=get_random_bg_color)
    is_deleted = models.BooleanField(_('Is deleted'), db_index=True, default=False)
    language = models.CharField(_('Language'), choices=settings.LANGUAGES, default="fr", max_length=255)
    last_update_at = models.DateTimeField(auto_now_add=True)
    last_update_by = models.ForeignKey('User', related_name='last_modified_users', on_delete=models.SET_NULL, null=True)
    mobile_phone = models.CharField(_('Mobile phone number'), blank=True, max_length=255, null=True, unique=True)
    mobile_phone_is_valid = models.BooleanField(_('Mobile phone is valid'), default=False)
    mobile_phone_is_validated = models.BooleanField(_('Mobile phone is validated'), db_index=True, default=False)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def language_name(self):
        """
            :return: return the name of the current language
        """
        return settings.LANGUAGES_DICT.get(self.language, "---")

    def to_dict(self):
        """
            :return: return a representation of current instance as an object
        """
        user = {
            "address": self.address,
            "birthday": self.birthday,
            "cin": self.cin,
            "country_code": self.country_code,
            "country_name": self.country_name,
            "created_at": self.created_at,
            "created_by_id": self.created_by_id,
            "email": self.email,
            "email_is_validated": self.email_is_validated,
            "first_name": self.first_name,
            "gender": self.gender,
            "id": self.id,
            "image_url": self.image_url,
            "initials_bg_color": self.initials_bg_color,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "language": self.language,
            "language_name": self.language_name,
            "last_name": self.last_name,
            "last_update_at": self.last_update_at,
            "last_update_by_id": self.last_update_by_id,
            "mobile_phone": self.mobile_phone,
            "mobile_phone_is_valid": self.mobile_phone_is_valid,
            "mobile_phone_is_validated": self.mobile_phone_is_validated,
            "username": self.username,
        }
        return user


class UserEmailConfirmationKey(models.Model):
    """
        UserEmailConfirmationKey represent the relationship between each user with his email confirmation key.
        :attribute: creation_time: DateTimeField represent the time when the key is created.
        :attribute: key: CharField represent a random key for confirm email.
        :attribute: user: ForeignKey represent the the relationship between the user and the keys.
    """
    class Meta(object):
        db_table = "remedial_teaching_user_email_confirmation_key"
        ordering = ["creation_time"]
        verbose_name = _("User email confirmation key")
        verbose_name_plural = _("Users emails confirmation keys")

    creation_time = models.DateTimeField(_('Creation time'), db_index=True, auto_now_add=True)
    key = models.CharField(_('Key'), db_index=True, default="", max_length=255)
    user = models.ForeignKey(User, related_name='email_confirmation_keys', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + "_" + self.key

    @property
    def is_expired(self):
        """
            :return: return True if timedelta between creation time and now is greater than settings.EMAIL_CONFIRMATION_KEY_EXPIRATION_MINUTES
        """
        diff = datetime.datetime.now().astimezone() - self.creation_time
        return ((diff.days * 24 * 3600) + diff.seconds) / 60 > settings.EMAIL_CONFIRMATION_KEY_EXPIRATION_MINUTES

    @classmethod
    def create(cls, user):
        """
            :param user: The user that will be linked to the email confirmation key
            :return: return an instance of UserEmailConfirmationKey with a generation confirmation key
        """
        key = user.email + uuid.uuid4().hex
        return cls.objects.create(key=key, user=user)

