# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class AccountTypeService(models.Model):
    """
        AccountTypeService represent the types-services of accounts of each user.
    """
    class Meta(object):
        db_table = "healthkools_account_type_service"
        ordering = ["type", "service"]
        verbose_name = _("Account type service")
        verbose_name_plural = _("Accounts types services")

    TYPES = (
        ("assistant", _("Assistant")),
        ("doctor", _("Doctor")),
        ("director", _("Director")),
        ("patient", _("Patient")),
        ("technician", _("Technician")),
        ("other", _("Other"))
    )
    TYPES_DICT = {
        "assistant": _("Assistant"),
        "doctor": _("Doctor"),
        "director": _("Director"),
        "patient": _("Patient"),
        "technician": _("Technician"),
        "other": _("Other")
    }
    SERVICES = (
        ("hospital", _("Hospital")),
        ("laboratory", _("Laboratory")),
        ("other", _("Other"))
    )
    SERVICES_DICT = {
        "hospital": _("Hospital"),
        "laboratory": _("Laboratory"),
        "other": _("Other")
    }

    type = models.CharField(_('Type'), choices=TYPES, default="other", max_length=255)
    service = models.CharField(_('Service'), choices=SERVICES, default="other", max_length=255)

    def __str__(self):
        return self.type_name + "_" + self.service_name

    @property
    def service_name(self):
        return self.SERVICES_DICT.get(self.service, "---")

    @property
    def type_name(self):
        return self.TYPES_DICT.get(self.type, "---")

    def to_dict(self):
        res = {
            "id": self.id,
            "service": self.service,
            "service_name": self.service_name,
            "type": self.type,
            "type_name": self.type_name,
        }
        return res


class User(AbstractUser):
    """
        HUser represent the user model.
    """
    class Meta(object):
        db_table = "healthkools_user"
        ordering = ["username"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    GENDERS = (
        ("", _("Select")),
        ("f", _("Female")),
        ("m", _("Male")),
    )
    accounts_types_services = models.ManyToManyField(AccountTypeService, related_name='users', through="UserAccountTypeService")
    country_code = models.CharField(_('Country code'), default="", max_length=10)
    country_name = models.CharField(_('Country name'), default="", max_length=255)
    email_is_valid = models.BooleanField(_('Email is valid'), default=False)
    gender = models.CharField(_('Gender'), choices=GENDERS, default="", max_length=10)
    language = models.CharField(_('Language'), choices=settings.LANGUAGES, default="fr", max_length=255)
    phone = models.CharField(_('Phone number'), blank=True, max_length=255, null=True)
    phone_is_valid = models.BooleanField(_('Phone is valid'), default=False)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def language_name(self):
        return settings.LANGUAGES_DICT.get(self.language, "---")

    def add_account_type_service(self, accounts_types_services=[], ids=[]):
        return self.accounts_types_services.add(*([account_type_service.id for account_type_service in accounts_types_services] if not ids else ids))

    def remove_account_type_service(self, accounts_types_services=[], ids=[]):
        return self.accounts_types_services.remove(*([account_type_service.id for account_type_service in accounts_types_services] if not ids else ids))

    def to_dict(self, get_accounts_types_services=False):
        res = {
            "country_code": self.country_code,
            "country_name": self.country_name,
            "email": self.email,
            "email_is_valid": self.email_is_valid,
            "first_name": self.first_name,
            "gender": self.gender,
            "id": self.id,
            "is_active": self.is_active,
            "language": self.language,
            "language_name": self.language_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "phone_is_valid": self.phone_is_valid,
            "username": self.username,
        }
        if get_accounts_types_services:
            res["accounts_types_services"] = [account_type_service.to_dict() for account_type_service in self.accounts_types_services.filter()]
        return res


class UserAccountTypeService(models.Model):
    """
        UserAccountType represent the relationship between each user with each account_type.
    """
    class Meta(object):
        db_table = "healthkools_user_account_type_service"
        ordering = ["user__username", "account_type_service__type", "account_type_service__service"]
        verbose_name = _("User account type service")
        verbose_name_plural = _("Users accounts types services")

    account_type_service = models.ForeignKey(AccountTypeService, related_name='my_users_relationship', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='my_accounts_types_services_relationship', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + "_" + self.account_type_service.__str__()
