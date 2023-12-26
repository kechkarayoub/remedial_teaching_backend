# -*- coding: utf-8 -*-
import datetime
from .models import *
from utils.utils import BG_COLORS_CHOICES
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from user.models import User
import json
import os


class EstablishmentModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(EstablishmentModelTests, self).__init__(*args, **kwargs)
        self.admin = None
        self.establishment_group = None

    def setUp(self):
        self.admin = User(username="administrator")
        self.admin.save()
        self.establishment_group = EstablishmentGroup(name="Group")
        self.establishment_group.save()

    def test___str__(self):
        establishment = Establishment(created_by=self.admin, establishment_group=self.establishment_group, last_update_by=self.admin, name="School1")
        establishment.save()
        str_ = establishment.__str__()
        self.assertEqual(str_, establishment.type_name + "_" + establishment.name)

    def test_to_dict(self):
        establishment = Establishment(
            address="address", address_ar="address_ar", city="city", created_by=self.admin, email="email@yopmail.com", fax="+212522xxxxxx",
            establishment_group=self.establishment_group, fax_is_valid=True, last_update_by=self.admiun,  logo_url="logo_url", name="name", name_ar="name_ar", type="school",
            website_url="localhost"
        )
        establishment.save()
        object_dict = establishment.to_dict()
        created_at = object_dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = object_dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(object_dict["address"], "address")
        self.assertEqual(object_dict["address_ar"], "address_ar")
        self.assertEqual(object_dict["city"], "city")
        self.assertEqual(object_dict["created_by_id"], self.admin.id)
        self.assertEqual(object_dict["email"], "email@yopmail.com")
        self.assertEqual(object_dict["fax"], "+212522xxxxxx")
        self.assertEqual(object_dict["fax_is_valid"], True)
        self.assertEqual(object_dict["fax_is_validated"], False)
        self.assertEqual(object_dict["id"], 1)
        self.assertEqual(object_dict["last_update_by"], self.admin.id)
        self.assertEqual(object_dict["logo_url"], "logo_url")
        self.assertEqual(object_dict["mobile_phone"], None)
        self.assertEqual(object_dict["mobile_phone_is_valid"], False)
        self.assertEqual(object_dict["mobile_phone_is_validated"], False)
        self.assertEqual(object_dict["name"], "name")
        self.assertEqual(object_dict["name_ar"], "name_ar")
        self.assertEqual(object_dict["phone"], None)
        self.assertEqual(object_dict["phone_is_valid"], False)
        self.assertEqual(object_dict["phone_is_validated"], False)
        self.assertEqual(object_dict["phone2"], None)
        self.assertEqual(object_dict["phone2_is_valid"], False)
        self.assertEqual(object_dict["phone2_is_validated"], False)
        self.assertEqual(object_dict["type"], "school")
        self.assertEqual(object_dict["type_name"], _("School"))
        self.assertEqual(object_dict["website_url"], "localhost")
        self.assertEqual(len(object_dict.keys()), 27)
        self.assertFalse(object_dict["is_deleted"])
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(object_dict["is_active"])

    def test_type_name(self):
        establishment = Establishment(name="School1")
        establishment.save()
        establishment2 = Establishment(name="School2", type="school")
        establishment2.save()
        establishment3 = Establishment(name="School1", type="other")
        establishment3.save()
        self.assertEqual(establishment.type_name, _("School"))
        self.assertEqual(establishment2.type_name, _("School"))
        self.assertEqual(establishment3.type_name, _("Other_"))


class EstablishmentGroupModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(EstablishmentGroupModelTests, self).__init__(*args, **kwargs)
        self.admin = None

    def setUp(self):
        self.admin = User(username="administrator")
        self.admin.save()

    def test___str__(self):
        establishment_group = EstablishmentGroup(created_by=self.admin, last_update_by=self.admin, name="Group1")
        establishment_group.save()
        str_ = establishment_group.__str__()
        self.assertEqual(str_, establishment_group.name)

    def test_to_dict(self):
        establishment_group = EstablishmentGroup(
            created_by=self.admin, last_update_by=self.admiun,
            logo_url="logo_url", name="name", name_ar="name_ar"
        )
        establishment_group.save()
        object_dict = establishment_group.to_dict()
        created_at = object_dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = object_dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(object_dict["created_by_id"], self.admin.id)
        self.assertEqual(object_dict["id"], 1)
        self.assertEqual(object_dict["last_update_by"], self.admin.id)
        self.assertEqual(object_dict["logo_url"], "logo_url")
        self.assertEqual(object_dict["name"], "name")
        self.assertEqual(object_dict["name_ar"], "name_ar")
        self.assertEqual(len(object_dict.keys()), 27)
        self.assertFalse(object_dict["is_deleted"])
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(object_dict["is_active"])


class EstablishmentUserModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(EstablishmentUserModelTests, self).__init__(*args, **kwargs)
        self.admin = None

    def setUp(self):
        self.admin = User(username="administrator")
        self.admin.save()

    def test___str__(self):
        establishment = Establishment.objects.create(name="School", type="school")
        user = User.objects.create(first_name="first_name", last_name="last_name", username="test_username", )
        # establishment_user = EstablishmentUser(email='email@domain.com', establishment=establishment, user=user)
        establishment_user = EstablishmentUser(establishment=establishment, user=user)
        establishment_user.save()
        str_ = establishment_user.__str__()
        # self.assertEqual(str_, establishment.__str__() + '_' + user.__str__())
        self.assertEqual(str_, "1")

    def test_to_dict(self):
        establishment = Establishment.objects.create(name="School", type="school")
        user = User.objects.create(username="test_username", last_name="last_name", first_name="first_name")
        establishment_user = EstablishmentUser(
            account_type="assistant", created_by=self.admin, email='email@domain.com', establishment=establishment, first_name="first_name",
            is_accepted=True, last_name="last_name", last_update_by=self.admin, user=user,
        )
        establishment_user.save()
        object_dict = establishment_user.to_dict()
        created_at = object_dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = object_dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(object_dict["address"], "")
        self.assertIsNone(object_dict["birthday"])
        self.assertEqual(object_dict["country_code"], "")
        self.assertEqual(object_dict["country_name"], "")
        self.assertEqual(object_dict["created_by_id"], None)
        self.assertEqual(object_dict["email"], 'email@domain.com')
        self.assertEqual(object_dict["email_is_accepted"], False)
        self.assertEqual(object_dict["establishment_id"], 1)
        self.assertEqual(object_dict["first_name"], "first_name")
        self.assertEqual(object_dict["gender"], "")
        self.assertEqual(object_dict["id"], 1)
        self.assertEqual(object_dict["image_url"], "")
        self.assertEqual(object_dict["is_accepted"], True)
        self.assertEqual(object_dict["last_name"], "last_name")
        self.assertEqual(object_dict["last_update_by"], None)
        self.assertEqual(object_dict["mobile_phone"], None)
        self.assertEqual(object_dict["mobile_phone_is_valid"], False)
        self.assertEqual(object_dict["mobile_phone_is_accepted"], False)
        self.assertEqual(object_dict["user_id"], 1)
        self.assertEqual(len(object_dict.keys()), 22)
        self.assertFalse(object_dict["is_deleted"])
        self.assertIn(object_dict["initials_bg_color"], BG_COLORS_CHOICES)
        self.assertNotEqual(object_dict["initials_bg_color"], "")
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(object_dict["is_active"])

