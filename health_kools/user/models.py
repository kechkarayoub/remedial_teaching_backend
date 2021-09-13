# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AccountTypeService(models.Model):
    """
        AccountTypeService represent the types-services of accounts of each user.
    """
    class Meta(object):
        db_table = "healthkools_account_type_service"
        ordering = ["type", "service"]

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
        return self.SERVICES_DICT[self.service]

    @property
    def type_name(self):
        return self.TYPES_DICT[self.type]

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
        db_table = "healthkools_h_user"
        ordering = ["username"]

    accounts_types_services = models.ManyToManyField(AccountTypeService, related_name='users', through="UserAccountTypeService")
    email_is_valid = models.BooleanField(_('Email is valid'), default=False)
    phone = models.CharField(_('Phone number'), blank=True, max_length=255, null=True)
    phone_is_valid = models.BooleanField(_('Phone address'), default=False)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class UserAccountTypeService(models.Model):
    """
        UserAccountType represent the relationship between each user with each account_type.
    """
    class Meta(object):
        db_table = "healthkools_user_account_type_service"
        ordering = ["user__username", "account_type_service__type", "account_type_service__service"]

    account_type_service = models.ForeignKey(AccountTypeService, related_name='my_users_relationship', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='my_accounts_types_services_relationship', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + "_" + self.account_type_service.__str__()

    def to_dict(self):
        res = {
            "email": self.email,
            "email_is_valid": self.email_is_valid,
            "first_name": self.first_name,
            "id": self.id,
            "is_active": self.is_active,
            "is_staff": self.is_staff,
            "last_name": self.last_name,
            "phone": self.phone,
            "phone_is_valid": self.phone_is_valid,
            "username": self.username,
        }
        return res
