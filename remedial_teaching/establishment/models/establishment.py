# -*- coding: utf-8 -*-
import datetime
import uuid

from .levels_subjects import Cycle
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from colorfield.fields import ColorField
from user.models import User
from utils.utils import get_random_bg_color


class EstablishmentGroup(models.Model):
    """
        EstablishmentGroup represent the establishment to manage.
        :attribute: created_at: DateTimeField represent the time when the establishment is created.
        :attribute: created_by: ForeignKey represent the creator of the establishment.
        :attribute: is_active: BooleanField represent if the establishment is active or not
        :attribute: is_deleted: BooleanField represent if the establishment is deleted or not
        :attribute: last_update_at: DateTimeField represent the time of last modification of establishment.
        :attribute: last_update_by: ForeignKey represent the last updater of the object.
        :attribute: logo_url: CharField represent the logo url of the establishment
        :attribute: name: CharField represent the name of the establishment
        :attribute: name_ar: CharField represent the arabic name of the establishment
    """
    class Meta(object):
        db_table = "remedial_teaching_establishment_group"
        ordering = ["name"]
        verbose_name = _("Establishment group")
        verbose_name_plural = _("Establishments groups")

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_establishments_groups', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(_('Is active'), db_index=True, default=True)
    is_deleted = models.BooleanField(_('Is deleted'), db_index=True, default=False)
    last_update_at = models.DateTimeField(auto_now_add=True)
    last_update_by = models.ForeignKey(User, related_name='last_modified_establishments_groups', on_delete=models.SET_NULL, null=True)
    logo_url = models.CharField(_('Logo url'), blank=True, max_length=512, null=True)
    name = models.CharField(_('Name'), blank=False, default="", db_index=True, max_length=255, null=False)
    name_ar = models.CharField(_('Name (ar)'), blank=True, default="", max_length=255, null=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        """
            :return: return a representation of current instance as an object
        """
        establishment_group = {
            "created_at": self.created_at,
            "created_by_id": self.created_by_id,
            "id": self.id,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "last_update_at": self.last_update_at,
            "last_update_by_id": self.last_update_by_id,
            "logo_url": self.logo_url,
            "name": self.name,
            "name_ar": self.name_ar,
        }
        return establishment_group


class Establishment(models.Model):
    """
        Establishment represent the establishment to manage.
        :attribute: address: CharField represent the address of the establishment
        :attribute: address_ar: CharField represent the arabic address of the establishment
        :attribute: city: CharField represent the city of the establishment
        :attribute: created_at: DateTimeField represent the time when the establishment is created.
        :attribute: created_by: ForeignKey represent the creator of the establishment.
        :attribute: email: CharField represent the email of the establishment
        :attribute: establishment_group: ForeignKey represent the establishment group of the establishment.
        :attribute: fax: CharField represent the number of fax of the establishment
        :attribute: fax_is_valid: BooleanField represent if the fax is valid or not
        :attribute: fax_is_validated: BooleanField represent if the fax is validated or not
        :attribute: is_active: BooleanField represent if the establishment is valid or not
        :attribute: is_deleted: BooleanField represent if the establishment is deleted or not
        :attribute: last_update_at: DateTimeField represent the time of last modification of establishment.
        :attribute: last_update_by: ForeignKey represent the last updater of the object.
        :attribute: logo_url: CharField represent the logo url of the establishment
        :attribute: mobile_phone: CharField represent the number of mobile phone of the establishment
        :attribute: mobile_phone_is_valid: BooleanField represent if the mobile phone is valid or not
        :attribute: mobile_phone_is_validated: BooleanField represent if the mobile phone is validated or not
        :attribute: name: CharField represent the name of the establishment
        :attribute: name_ar: CharField represent the arabic name of the establishment
        :attribute: phone: CharField represent the number of phone of establishment
        :attribute: phone_is_valid: BooleanField represent if the phone is valid or not
        :attribute: phone_is_validated: BooleanField represent if the phone is validated or not
        :attribute: phone2: CharField represent the second of phone of establishment
        :attribute: phone2_is_valid: BooleanField represent if the phone2 is valid or not
        :attribute: phone2_is_validated: BooleanField represent if the phone2 is validated or not
        :attribute: type: CharField represent the type of the establishment
        :attribute: website_url: CharField represent the website url of the establishment
    """
    class Meta(object):
        db_table = "remedial_teaching_establishment"
        ordering = ["name"]
        verbose_name = _("Establishment")
        verbose_name_plural = _("Establishments")
        unique_together = ('establishment_group', 'name', 'type',)

    TYPES = (
        ("school", _("School")),
        ("other", _("Other")),
    )
    TYPES_DICT = {
        "school": _("School"),
        "other": _("Other"),
    }

    address = models.TextField(_('Address'), blank=True, default="")
    address_ar = models.TextField(_('Address (ar)'), blank=True, default="")
    city = models.CharField(_('City'), blank=True, default="", max_length=255)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_establishments', on_delete=models.SET_NULL, null=True)
    email = models.CharField(_('Email'), blank=True, db_index=True, max_length=255, null=True)
    establishment_group = models.ForeignKey(EstablishmentGroup, related_name='establishments', on_delete=models.CASCADE)
    fax = models.CharField(_('Fax'), blank=True, max_length=255, null=True)
    fax_is_valid = models.BooleanField(_('Fax is valid'), default=False)
    fax_is_validated = models.BooleanField(_('Fax is validated'), db_index=True, default=False)
    is_active = models.BooleanField(_('Is active'), db_index=True, default=True)
    is_deleted = models.BooleanField(_('Is deleted'), db_index=True, default=False)
    last_update_at = models.DateTimeField(auto_now_add=True)
    last_update_by = models.ForeignKey(User, related_name='last_modified_establishments', on_delete=models.SET_NULL, null=True)
    logo_url = models.CharField(_('Logo url'), blank=True, max_length=512, null=True)
    mobile_phone = models.CharField(_('Mobile phone'), blank=True, max_length=255, null=True)
    mobile_phone_is_valid = models.BooleanField(_('Mobile phone is valid'), db_index=True, default=False)
    mobile_phone_is_validated = models.BooleanField(_('Mobile phone is validated'), db_index=True, default=False)
    name = models.CharField(_('Name'), blank=False, db_index=True, default="", max_length=255, null=False)
    name_ar = models.CharField(_('Name (ar)'), blank=True, default="", max_length=255, null=True)
    phone = models.CharField(_('Phone number'), blank=True, db_index=True, max_length=255, null=True)
    phone_is_valid = models.BooleanField(_('Phone is valid'), db_index=True, default=False)
    phone_is_validated = models.BooleanField(_('Phone is validated'), db_index=True, default=False)
    phone2 = models.CharField(_('Phone2 number'), blank=True, db_index=True, max_length=255, null=True)
    phone2_is_valid = models.BooleanField(_('Phone2 is valid'), db_index=True, default=False)
    phone2_is_validated = models.BooleanField(_('Phone2 is validated'), db_index=True, default=False)
    type = models.CharField(_('Type'), choices=TYPES, db_index=True, default="school", max_length=255)
    website_url = models.CharField(_('Website url'), blank=True, default="", max_length=255, null=True)

    def __str__(self):
        return self.type_name + "_" + self.name

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
        establishment = {
            "address": self.address,
            "address_ar": self.address_ar,
            "city": self.city,
            "created_at": self.created_at,
            "created_by_id": self.created_by_id,
            "email": self.email,
            "establishment_group_id": self.establishment_group_id,
            "fax": self.fax,
            "fax_is_valid": self.fax_is_valid,
            "fax_is_validated": self.fax_is_validated,
            "id": self.id,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "last_update_at": self.last_update_at,
            "last_update_by_id": self.last_update_by_id,
            "logo_url": self.logo_url,
            "mobile_phone": self.mobile_phone,
            "mobile_phone_is_valid": self.mobile_phone_is_valid,
            "mobile_phone_is_validated": self.mobile_phone_is_validated,
            "name": self.name,
            "name_ar": self.name_ar,
            "phone": self.phone,
            "phone_is_valid": self.phone_is_valid,
            "phone_is_validated": self.phone_is_validated,
            "phone2": self.phone2,
            "phone2_is_valid": self.phone2_is_valid,
            "phone2_is_validated": self.phone2_is_validated,
            "type": self.type,
            "type_name": self.type_name,
            "website_url": self.website_url,
        }
        return establishment


class EstablishmentCycle(models.Model):
    """
        Cycle represent the scholar cycles.
        :attribute: created_at: DateTimeField represent the time when the object is created.
        :attribute: created_by: ForeignKey represent the creator of the object.
        :attribute: cycle: ForeignKey represent a cycle.
        :attribute: establishment: ForeignKey represent an establishment.
        :attribute: is_active: BooleanField represent if the object is active or not
        :attribute: last_update_at: DateTimeField represent the time of last modification of object.
        :attribute: last_update_by: ForeignKey represent the last updater of the object.
        :attribute: name: CharField represent the name of the object
        :attribute: name_ar: CharField represent the arabic name of the object
    """
    class Meta(object):
        db_table = "remedial_teaching_establishment_cycle"
        ordering = ["cycle__order"]
        unique_together = ('establishment', 'cycle', )
        verbose_name = _("Establishment-Cycle")
        verbose_name_plural = _("Establishments-Cycles")

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_establishments_cycles', on_delete=models.SET_NULL, null=True)
    cycle = models.ForeignKey(Cycle, related_name='my_establishments', on_delete=models.PROTECT)
    establishment = models.ForeignKey(Establishment, related_name='my_cycles', on_delete=models.PROTECT)
    is_active = models.BooleanField(_('Is active'), db_index=True, default=True)
    last_update_at = models.DateTimeField(auto_now_add=True)
    last_update_by = models.ForeignKey(User, related_name='last_modified_establishment_cycles', on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Name'), blank=False, default="", db_index=True, max_length=255, null=False, unique=True)
    name_ar = models.CharField(_('Name (ar)'), blank=True, default="", max_length=255, null=True)

    def __str__(self):
        return 'EstablishmentCycle_' + self.name + '_' + self.establishment.name

    def to_dict(self):
        """
            :return: return a representation of current instance as an object
        """
        cycle = {
            "created_at": self.created_at,
            "created_by_id": self.created_by_id,
            "cycle_id": self.cycle_id,
            "establishment_id": self.establishment_id,
            "id": self.id,
            "is_active": self.is_active,
            "last_update_at": self.last_update_at,
            "last_update_by_id": self.last_update_by_id,
            "name": self.name,
            "name_ar": self.name_ar,
        }
        return cycle


class EstablishmentUser(models.Model):
    """
        User represent the establishment user relationship model.
        :attribute: account_type: TextfieldField represent the type of relationship between the user and the establishment,
            it can be one or more from ACCOUNT_TYPES joined by '_'
        :attribute: address: CharField represent the address of user
        :attribute: birthday: DateField represent the birthday of user
        :attribute: country_code: CharField represent the country code of user
        :attribute: country_name: CharField represent the country name of user
        :attribute: created_at: DatetimeField represent the time of object creation
        :attribute: created_by: ForeignKey represent the creator of the object.
        :attribute: email: CharField represent the email of the user
        :attribute: email_is_accepted: BooleanField represent if the users email is accepted by user or not
        :attribute: establishment: ForeignKey key represent the establishment in the relationship
        :attribute: first_name: CharField represent the first name of user
        :attribute: gender: CharField represent the gender of user
        :attribute: image_url: CharField represent the image of user
        :attribute: initials_bg_color: CharField represent the background color of user's initials
        :attribute: is_accepted: BooleanField represent if the relationship is accepted by the user or not
        :attribute: is_active: BooleanField represent if the relationship is active or not
        :attribute: is_deleted: BooleanField represent if the item is deleted by user or not
        :attribute: last_name: CharField represent the last name of user
        :attribute: last_update_at: DatetimeField represent the last time the object updated
        :attribute: last_update_by: ForeignKey represent the last updater of the object.
        :attribute: massar_code: CharField represent the massar code of user
        :attribute: mobile_phone: CharField represent the mobile_phone of user
        :attribute: mobile_phone_is_accepted: BooleanField represent user mobile_phone is accepted by user or not
        :attribute: mobile_phone_is_valid: BooleanField represent user mobile_phone is valid or not
        :attribute: user: ForeignKey key represent the user in the relationship
    """
    class Meta(object):
        db_table = "remedial_teaching_establishment_user"
        ordering = ["last_name", "first_name"]
        verbose_name = _("Establishment user relationship")
        verbose_name_plural = _("Establishment user relationships")
        unique_together = ('establishment', 'user',)

    ACCOUNT_TYPES = (
        ("admin", _("Administrator")),
        ("assistant", _("Assistant")),
        ("director", _("Director")),
        ("parent", _("Parent")),
        ("student", _("Student")),
        ("other", _("Other"))
    )
    ACCOUNT_TYPES_DICT = {
        "admin": _("Administrator"),
        "assistant": _("Assistant"),
        "director": _("Director"),
        "parent": _("Parent"),
        "student": _("Student"),
        "other": _("Other")
    }
    GENDERS = (
        ("", _("Select")),
        ("f", _("Female")),
        ("m", _("Male")),
    )
    account_type = models.CharField(
        _('Account type'), db_index=True, default="", max_length=512,
        help_text="One or more from [admin, assistant, director, parent, student, other] joined by '_'"
    )
    address = models.TextField(_('Address'), blank=True, default="")
    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    cin = models.CharField(_('CIN'), blank=True, default="", db_index=True, max_length=15, null=False)
    country_code = models.CharField(_('Country code'), blank=True, default="", max_length=10)
    country_name = models.CharField(_('Country name'), blank=True, default="", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, related_name='created_users_establishments_relationships', on_delete=models.SET_NULL, null=True)
    email = models.CharField(_('Email'), db_index=True, max_length=255)
    email_is_accepted = models.BooleanField(_('Email is accepted'), db_index=True, default=False)
    establishment = models.ForeignKey(Establishment, related_name='users_relationships', on_delete=models.CASCADE)
    first_name = models.CharField(_('First name'), blank=False, db_index=True, default="", max_length=255, null=False)
    gender = models.CharField(_('Gender'), blank=True, choices=GENDERS, db_index=True, default="", max_length=10)
    image_url = models.CharField(_('Image url'), blank=True, default="", max_length=512)
    initials_bg_color = ColorField(_('Initials background color'), default=get_random_bg_color)
    is_accepted = models.BooleanField(_('Is accepted'), db_index=True, default=True)
    is_active = models.BooleanField(_('Is active'), db_index=True, default=True)
    is_deleted = models.BooleanField(_('Is deleted'), db_index=True, default=False)
    last_name = models.CharField(_('Last name'), blank=False, db_index=True, default="", max_length=255, null=False)
    last_update_at = models.DateTimeField(auto_now_add=True)
    last_update_by = models.ForeignKey(User, related_name='last_modified_users_establishments_relationships', on_delete=models.SET_NULL, null=True)
    massar_code = models.CharField(_('Massar code'), blank=True, default="", db_index=True, max_length=20, null=False)
    mobile_phone = models.CharField(_('Mobile phone number'), blank=True, max_length=255, null=True)
    mobile_phone_is_accepted = models.BooleanField(_('Mobile phone is accepted'), db_index=True, default=False)
    mobile_phone_is_valid = models.BooleanField(_('Mobile phone is valid'), default=False)
    user = models.ForeignKey(User, related_name='establishments_relationships', on_delete=models.CASCADE)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.establishment.__str__() + "_" + self.user.__str__()

    def to_dict(self):
        """
            :return: return a representation of current instance as an object
        """
        establishment_user = {
            "account_type": self.account_type,
            "address": self.address,
            "birthday": self.birthday,
            "cin": self.cin,
            "country_code": self.country_code,
            "country_name": self.country_name,
            "created_at": self.created_at,
            "email": self.email,
            "created_by_id": self.created_by_id,
            "email_is_accepted": self.email_is_accepted,
            "establishment_id": self.establishment_id,
            "first_name": self.first_name,
            "gender": self.gender,
            "id": self.id,
            "image_url": self.image_url,
            "initials_bg_color": self.initials_bg_color,
            "is_accepted": self.is_accepted,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "last_name": self.last_name,
            "last_update_at": self.last_update_at,
            "last_update_by_id": self.last_update_by_id,
            "massar_code": self.massar_code,
            "mobile_phone": self.mobile_phone,
            "mobile_phone_is_valid": self.mobile_phone_is_valid,
            "mobile_phone_is_accepted": self.mobile_phone_is_accepted,
            "user_id": self.user_id,
        }
        return establishment_user


class ScholarYear(models.Model):
    """
        ScholarYear represent the scholar years.
        :attribute: created_at: DateTimeField represent the time when the object is created.
        :attribute: created_by: ForeignKey represent the creator of the object.
        :attribute: date_start: DateField represent the start date of the scholar year.
        :attribute: date_end: DateField represent the end date of the scholar year.
        :attribute: is_active: BooleanField represent if the object is valid or not
        :attribute: is_current: BooleanField represent if the object is current scholar year or not
        :attribute: is_deleted: BooleanField represent if the object is deleted or not
        :attribute: last_update_at: DateTimeField represent the time of last modification of the object.
        :attribute: last_update_by: ForeignKey represent the last updater of the object.
        :attribute: name: CharField represent the name of the scholar year
        :attribute: order: IntegerField represent the order of the scholar year
        :attribute: short_name: CharField represent the short name of the scholar year
        :attribute: start_year: IntegerField represent the start year of the scholar year
    """
    class Meta(object):
        db_table = "remedial_teaching_scholar_year"
        ordering = ["order"]
        verbose_name = _("Scholar year")
        verbose_name_plural = _("Scholar years")

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_scholar_years', on_delete=models.SET_NULL, null=True)
    date_end = models.DateField(_('Date end'), db_index=True, null=False)
    date_start = models.DateField(_('Date start'), db_index=True, null=False)
    is_active = models.BooleanField(_('Is active'), db_index=True, default=True)
    is_current = models.BooleanField(_('Is current'), db_index=True, default=False)
    is_deleted = models.BooleanField(_('Is deleted'), db_index=True, default=False)
    last_update_at = models.DateTimeField(auto_now_add=True)
    last_update_by = models.ForeignKey(User, related_name='last_modified_scholar_years', on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Name'), blank=False, db_index=True, default="", max_length=255, unique=True)
    order = models.IntegerField(_('Order'), blank=False, db_index=True, null=False, unique=True)
    short_name = models.CharField(_('Short name'), blank=False, db_index=True, default="", max_length=255, unique=True)
    start_year = models.IntegerField(_('Start year'), blank=False, db_index=True, null=False, unique=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        """
            :return: return a representation of current instance as an object
        """
        scholar_year = {
            "created_at": self.created_at,
            "created_by_id": self.created_by_id,
            "date_end": self.date_end,
            "date_start": self.date_start,
            "id": self.id,
            "is_active": self.is_active,
            "is_current": self.is_current,
            "is_deleted": self.is_deleted,
            "last_update_at": self.last_update_at,
            "last_update_by_id": self.last_update_by_id,
            "name": self.name,
            "order": self.order,
            "short_name": self.short_name,
        }
        return scholar_year

