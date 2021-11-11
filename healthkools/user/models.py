# -*- coding: utf-8 -*-
import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class AccountTypeService(models.Model):
    """
        AccountTypeService represent the types-services of accounts of each user.
        :attribute: type: CharField represent the account type of services
        :attribute: service: CharField represent the service types
    """
    class Meta(object):
        db_table = "healthkools_account_type_service"
        ordering = ["type", "service"]
        verbose_name = _("Account type service")
        verbose_name_plural = _("Accounts types services")
        unique_together = ('service', 'type')

    TYPES = (
        ("assistant", _("Assistant")),
        ("doctor", _("Doctor")),
        ("director", _("Director")),
        ("nurse", _("Nurse")),
        ("patient", _("Patient")),
        ("technician", _("Technician")),
        ("other", _("Other"))
    )
    TYPES_DICT = {
        "assistant": _("Assistant"),
        "doctor": _("Doctor"),
        "director": _("Director"),
        "nurse": _("Nurse"),
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
        """
            :return: return the name of the current service
        """
        return self.SERVICES_DICT.get(self.service, "---")

    @property
    def type_name(self):
        """
            :return: return the name of the current type
        """
        return self.TYPES_DICT.get(self.type, "---")

    def to_dict(self):
        """
            :return: return a representation of current instance as an object
        """
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
        User represent the user model.
        :attribute: accounts_types_services: ManyToManyField represent the relationship between users and the accounts services
        :attribute: address: CharField represent the address of users
        :attribute: birthday: DateField represent the birthday of users
        :attribute: country_code: CharField represent the country code of users
        :attribute: country_name: CharField represent the country name of users
        :attribute: email_is_validated: BooleanField represent if the users email is validated or not
        :attribute: gender: CharField represent the gender of users
        :attribute: language: CharField represent the language of users
        :attribute: phone: CharField represent the phone of users
        :attribute: phone_is_valid: BooleanField represent users phone is valid or not
        :attribute: phone_is_validated: BooleanField represent users phone is validated or not
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
    address = models.CharField(_('Address'), default="", max_length=10)
    birthday = models.DateField(_('Birthday'), null=True)
    country_code = models.CharField(_('Country code'), blank=True, default="", max_length=10)
    country_name = models.CharField(_('Country name'), blank=True, default="", max_length=255)
    email_is_validated = models.BooleanField(_('Email is validated'), default=False)
    gender = models.CharField(_('Gender'), blank=True, choices=GENDERS, default="", max_length=10)
    language = models.CharField(_('Language'), choices=settings.LANGUAGES, default="fr", max_length=255)
    phone = models.CharField(_('Phone number'), blank=True, max_length=255, null=True)
    phone_is_valid = models.BooleanField(_('Phone is valid'), default=False)
    phone_is_validated = models.BooleanField(_('Phone is validated'), default=False)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def language_name(self):
        """
            :return: return the name of the current language
        """
        return settings.LANGUAGES_DICT.get(self.language, "---")

    def add_account_type_service(self, accounts_types_services=[], ids=[]):
        """
            :param accounts_types_services: accounts types services to link with the current user
            :param ids: ids of the accounts types services to link with the current user
            :return: None
        """
        self.accounts_types_services.add(*([account_type_service.id for account_type_service in accounts_types_services] if not ids else ids))

    def remove_account_type_service(self, accounts_types_services=[], ids=[]):
        """
            :param accounts_types_services: accounts types services to unlink with the current user
            :param ids: ids of the accounts types services to unlink with the current user
            :return: None
        """
        self.accounts_types_services.remove(*([account_type_service.id for account_type_service in accounts_types_services] if not ids else ids))

    def to_dict(self, get_accounts_types_services=False):
        """
            :param get_accounts_types_services: return accounts types services if get_accounts_types_services is True
            :return: return a representation of current instance as an object
        """
        res = {
            "address": self.address,
            "birthday": self.birthday,
            "country_code": self.country_code,
            "country_name": self.country_name,
            "email": self.email,
            "email_is_validated": self.email_is_validated,
            "first_name": self.first_name,
            "gender": self.gender,
            "id": self.id,
            "is_active": self.is_active,
            "language": self.language,
            "language_name": self.language_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "phone_is_valid": self.phone_is_valid,
            "phone_is_validated": self.phone_is_validated,
            "username": self.username,
        }
        if get_accounts_types_services:
            res["accounts_types_services"] = [account_type_service.to_dict() for account_type_service in self.accounts_types_services.filter()]
        return res

    def get_security_questions(self):
        """
            :return: return the security questions of the current user as a list of objects
        """
        return [sq.to_dict() for sq in self.my_security_questions.filter()]


class UserAccountTypeService(models.Model):
    """
        UserAccountType represent the relationship between each user with each account_type.
        :attribute: account_type_service: ForeignKey represent the relationship between the account type service and users
        :attribute: user: ForeignKey represent the the relationship between the user  and accounts types services
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


class UserEmailConfirmationKey(models.Model):
    """
        UserEmailConfirmationKey represent the relationship between each user with his email confirmation key.
        :attribute: creation_time: DateTimeField represent the time when the key is created.
        :attribute: key: CharField represent a random key for confirm email.
        :attribute: user: ForeignKey represent the the relationship between the user and the keys.
    """
    class Meta(object):
        db_table = "healthkools_user_email_confirmation_key"
        ordering = ["creation_time"]
        verbose_name = _("User email confirmation key")
        verbose_name_plural = _("Users emails confirmation keys")

    creation_time = models.DateTimeField(_('Creation time'), auto_now_add=True)
    key = models.CharField(_('Key'), default="", max_length=255)
    user = models.ForeignKey(User, related_name='my_email_confirmation_keys', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + "_" + self.key

    @property
    def is_expired(self):
        """
            :return: return True if timedelta between creation time and now is greater than settings.EMAIL_CONFIRMATION_KEY_EXPIRATION_MINUTES
        """
        diff = datetime.datetime.now().astimezone() - self.creation_time
        return diff.seconds / 60 > settings.EMAIL_CONFIRMATION_KEY_EXPIRATION_MINUTES

    @classmethod
    def create(cls, user):
        """
            :param user: The user that will be linked to the email confirmation key
            :return: return an instance of UserEmailConfirmationKey with a generation confirmation key
        """
        key = user.email + uuid.uuid4().hex
        return cls.objects.create(key=key, user=user)


class UserSecurityQuestion(models.Model):
    """
        UserSecurityQuestion represent the relationship between each user with security questions.
        :attribute: response: CharField represent a response of security question
        :attribute: security_question: CharField represent a security question
        :attribute: user: ForeignKey represent the the relationship between the user and question securities
    """
    class Meta(object):
        db_table = "healthkools_user_security_question"
        ordering = ["security_question"]
        verbose_name = _("User security question")
        verbose_name_plural = _("Users security questions")

    SECURITY_QUESTIONS = (
        ("what_did_you_want_to_be_bigger_when_you_were_a_kid", _("What did you want to be bigger when you were a kid?")),
        ("what_is_the_last_name_of_your_favorite_childhood_teacher", _("What is the last name of your favorite childhood teacher?")),
        ("what_is_your_birthday", _("What is your birthday?")),
        ("what_is_your_favorite_car", _("What is your favorite car?")),
        ("what_is_your_favorite_color", _("What is your favorite color?")),
        ("what_is_your_favorite_movie", _("What is your favorite movie?")),
        ("what_is_your_place_of_birth", _("What is your place of birth?")),
        ("z_other", _("Other"))
    )
    # SECURITY_QUESTIONS_DICT = {
    #     "what_did_you_want_to_be_bigger_when_you_were_a_kid": _("What did you want to be bigger when you were a kid?"),
    #     "what_is_the_last_name_of_your_favorite_childhood_teacher": _("What is the last name of your favorite childhood teacher?"),
    #     "what_is_your_birthday": _("What is your birthday?"),
    #     "what_is_your_favorite_car": _("What is your favorite car?"),
    #     "what_is_your_favorite_color": _("What is your favorite color?"),
    #     "what_is_your_favorite_movie": _("What is your favorite movie?"),
    #     "what_is_your_place_of_birth": _("What is your place of birth?"),
    #     "z_other": _("Other")
    # }
    SECURITY_QUESTIONS_LIST = [
        ["what_did_you_want_to_be_bigger_when_you_were_a_kid", "What did you want to be bigger when you were a kid?"],
        ["what_is_the_last_name_of_your_favorite_childhood_teacher", "What is the last name of your favorite childhood teacher?"],
        ["what_is_your_birthday", "What is your birthday?"],
        ["what_is_your_favorite_car", "What is your favorite car?"],
        ["what_is_your_favorite_color", "What is your favorite color?"],
        ["what_is_your_favorite_movie", "What is your favorite movie?"],
        ["what_is_your_place_of_birth", "What is your place of birth?"],
        ["z_other", "Other"]
    ]

    response = models.CharField(_('Response'), default="", max_length=255)
    security_question = models.CharField(_('Security question'), choices=SECURITY_QUESTIONS, default="z_other", max_length=255)
    user = models.ForeignKey(User, related_name='my_security_questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + "_" + self.security_question

    def to_dict(self):
        return {
            "id": self.id,
            "response": self.response,
            "security_question": self.security_question,
        }

    @classmethod
    def get_list_choices(cls):
        """
            :return: return a list of lists that contains security question label and name
        """
        return cls.SECURITY_QUESTIONS_LIST
