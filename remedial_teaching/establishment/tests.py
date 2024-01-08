# -*- coding: utf-8 -*-
from .models import *
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from user.models import User
from utils.utils import BG_COLORS_CHOICES


class CycleModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(CycleModelTests, self).__init__(*args, **kwargs)
        self.admin = None

    def setUp(self):
        self.admin = User(username="administrator", cin='adm')
        self.admin.save()

    def test___str__(self):
        cycle = Cycle(created_by=self.admin, last_update_by=self.admin, name="Primaire", order=1)
        cycle.save()
        str_ = cycle.__str__()
        self.assertEqual(str_, 'Cycle_' + cycle.name + '_' + str(cycle.id))

    def test_to_dict(self):
        cycle1 = Cycle(created_by=self.admin, last_update_by=self.admin, name="Primaire", order=1)
        cycle1.save()
        object_dict = cycle1.to_dict()
        created_at = object_dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = object_dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(len(object_dict.keys()), 9)
        self.assertEqual(object_dict["created_by_id"], self.admin.id)
        self.assertEqual(object_dict["id"], 1)
        self.assertEqual(object_dict["last_update_by_id"], self.admin.id)
        self.assertEqual(object_dict["name"], "Primaire")
        self.assertEqual(object_dict["name_ar"], "")
        self.assertEqual(object_dict["order"], 1)
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(object_dict["is_active"])

    def test_unique_cycle(self):
        Cycle.objects.create(created_by=self.admin, last_update_by=self.admin, name="Primaire", order=1)
        with self.assertRaises(IntegrityError) as name_context:
            Cycle.objects.create(created_by=self.admin, last_update_by=self.admin, name="Primaire", order=2)
        self.assertIn('UNIQUE constraint failed', str(name_context.exception))
        transaction.set_rollback(False)
        with self.assertRaises(IntegrityError) as order_context:
            Cycle.objects.create(created_by=self.admin, last_update_by=self.admin, name="Primaire_", order=1)
        self.assertIn('UNIQUE constraint failed', str(order_context.exception))
        transaction.set_rollback(False)
        with self.assertRaises(IntegrityError) as order_not_null_context:
            Cycle.objects.create(created_by=self.admin, last_update_by=self.admin)
        self.assertIn('NOT NULL constraint failed: remedial_teaching_cycle.order', str(order_not_null_context.exception))
        transaction.set_rollback(True)


class EstablishmentModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(EstablishmentModelTests, self).__init__(*args, **kwargs)
        self.admin = None
        self.establishment_group = None

    def setUp(self):
        self.admin = User(username="administrator", cin='adm')
        self.admin.save()
        self.establishment_group = EstablishmentGroup(name="Group")
        self.establishment_group.save()

    def test___str__(self):
        establishment = Establishment(created_by=self.admin, establishment_group=self.establishment_group, last_update_by=self.admin, name="School1")
        establishment.save()
        str_ = establishment.__str__()
        self.assertEqual(str_, establishment.type_name + "_" + establishment.name)

    def test_to_dict(self):
        establishment1 = Establishment(
            address="address", address_ar="address_ar", city="city", created_by=self.admin, email="email@yopmail.com", fax="+212522xxxxxx",
            establishment_group=self.establishment_group, fax_is_valid=True, last_update_by=self.admin,  logo_url="logo_url", name="name", name_ar="name_ar", type="school",
            website_url="localhost"
        )
        establishment1.save()
        object_dict = establishment1.to_dict()
        created_at = object_dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = object_dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(len(object_dict.keys()), 30)
        self.assertEqual(object_dict["address"], "address")
        self.assertEqual(object_dict["address_ar"], "address_ar")
        self.assertEqual(object_dict["city"], "city")
        self.assertEqual(object_dict["created_by_id"], self.admin.id)
        self.assertEqual(object_dict["email"], "email@yopmail.com")
        self.assertEqual(object_dict["fax"], "+212522xxxxxx")
        self.assertEqual(object_dict["fax_is_valid"], True)
        self.assertEqual(object_dict["fax_is_validated"], False)
        self.assertEqual(object_dict["id"], 1)
        self.assertEqual(object_dict["last_update_by_id"], self.admin.id)
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
        self.assertFalse(object_dict["is_deleted"])
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(object_dict["is_active"])

    def test_type_name(self):
        establishment2 = Establishment(establishment_group=self.establishment_group, name="School1")
        establishment2.save()
        establishment2 = Establishment(establishment_group=self.establishment_group, name="School2", type="school")
        establishment2.save()
        establishment3 = Establishment(establishment_group=self.establishment_group, name="School1", type="other")
        establishment3.save()
        self.assertEqual(establishment2.type_name, _("School"))
        self.assertEqual(establishment2.type_name, _("School"))
        self.assertEqual(establishment3.type_name, _("Other"))


class EstablishmentGroupModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(EstablishmentGroupModelTests, self).__init__(*args, **kwargs)
        self.admin = None

    def setUp(self):
        self.admin = User(username="administrator", cin='adm')
        self.admin.save()

    def test___str__(self):
        establishment_group = EstablishmentGroup(created_by=self.admin, last_update_by=self.admin, name="Group1")
        establishment_group.save()
        str_ = establishment_group.__str__()
        self.assertEqual(str_, establishment_group.name)

    def test_to_dict(self):
        establishment_group = EstablishmentGroup(
            created_by=self.admin, last_update_by=self.admin,
            logo_url="logo_url", name="name", name_ar="name_ar"
        )
        establishment_group.save()
        object_dict = establishment_group.to_dict()
        created_at = object_dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = object_dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(len(object_dict.keys()), 10)
        self.assertEqual(object_dict["created_by_id"], self.admin.id)
        self.assertEqual(object_dict["id"], 1)
        self.assertEqual(object_dict["last_update_by_id"], self.admin.id)
        self.assertEqual(object_dict["logo_url"], "logo_url")
        self.assertEqual(object_dict["name"], "name")
        self.assertEqual(object_dict["name_ar"], "name_ar")
        self.assertFalse(object_dict["is_deleted"])
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(object_dict["is_active"])


class EstablishmentUserModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(EstablishmentUserModelTests, self).__init__(*args, **kwargs)
        self.admin = None
        self.establishment_group = None

    def setUp(self):
        self.admin = User(username="administrator", cin='adm')
        self.admin.save()
        self.establishment_group = EstablishmentGroup(name="Group")
        self.establishment_group.save()

    def test___str__(self):
        establishment1 = Establishment.objects.create(establishment_group=self.establishment_group, name="School", type="school")
        user = User.objects.create(first_name="first_name", last_name="last_name", username="test_username", )
        # establishment_user = EstablishmentUser(email='email@domain.com', establishment=establishment, user=user)
        establishment_user = EstablishmentUser(establishment=establishment1, user=user)
        establishment_user.save()
        str_ = establishment_user.__str__()
        self.assertEqual(str_, establishment1.__str__() + '_' + user.__str__())

    def test_to_dict(self):
        establishment2 = Establishment.objects.create(establishment_group=self.establishment_group, name="School", type="school")
        user = User.objects.create(username="test_username", last_name="last_name", first_name="first_name")
        establishment_user = EstablishmentUser(
            account_type="assistant", cin='cin', massar_code='massar_code', created_by=self.admin, email='email@domain.com', establishment=establishment2, first_name="first_name",
            is_accepted=True, last_name="last_name", last_update_by=self.admin, user=user,
        )
        establishment_user.save()
        object_dict = establishment_user.to_dict()
        created_at = object_dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = object_dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(len(object_dict.keys()), 27)
        self.assertEqual(object_dict["address"], "")
        self.assertIsNone(object_dict["birthday"])
        self.assertEqual(object_dict["country_code"], "")
        self.assertEqual(object_dict["country_name"], "")
        self.assertEqual(object_dict["cin"], 'cin')
        self.assertEqual(object_dict["created_by_id"], self.admin.id)
        self.assertEqual(object_dict["email"], 'email@domain.com')
        self.assertEqual(object_dict["email_is_accepted"], False)
        self.assertEqual(object_dict["establishment_id"], 1)
        self.assertEqual(object_dict["first_name"], "first_name")
        self.assertEqual(object_dict["gender"], "")
        self.assertEqual(object_dict["id"], 1)
        self.assertEqual(object_dict["image_url"], "")
        self.assertEqual(object_dict["is_accepted"], True)
        self.assertEqual(object_dict["last_name"], "last_name")
        self.assertEqual(object_dict["last_update_by_id"], self.admin.id)
        self.assertEqual(object_dict["massar_code"], 'massar_code')
        self.assertEqual(object_dict["mobile_phone"], None)
        self.assertEqual(object_dict["mobile_phone_is_valid"], False)
        self.assertEqual(object_dict["mobile_phone_is_accepted"], False)
        self.assertEqual(object_dict["user_id"], 2)
        self.assertFalse(object_dict["is_deleted"])
        self.assertIn(object_dict["initials_bg_color"], BG_COLORS_CHOICES)
        self.assertNotEqual(object_dict["initials_bg_color"], "")
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(object_dict["is_active"])

    def test_unique_establishment_user(self):
        establishment3 = Establishment.objects.create(establishment_group=self.establishment_group, name="School", type="school")
        user = User.objects.create(username="test_username", last_name="last_name", first_name="first_name")
        establishment_user = EstablishmentUser(
            account_type="assistant", created_by=self.admin, email='email@domain.com', establishment=establishment3, first_name="first_name",
            is_accepted=True, last_name="last_name", last_update_by=self.admin, user=user,
        )
        establishment_user.save()
        with self.assertRaises(IntegrityError) as context:
            establishment_user2 = EstablishmentUser(
                account_type="assistant", created_by=self.admin, email='email@domain.com', establishment=establishment3,
                first_name="first_name",
                is_accepted=True, last_name="last_name", last_update_by=self.admin, user=user,
            )
            establishment_user2.save()

        self.assertIn('UNIQUE constraint failed', str(context.exception))


class ScholarYearModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(ScholarYearModelTests, self).__init__(*args, **kwargs)
        self.admin = None

    def setUp(self):
        self.admin = User(username="administrator", cin='adm')
        self.admin.save()

    def test___str__(self):
        date_start = datetime.datetime.now()
        date_end = datetime.datetime.now()
        scholar_year = ScholarYear.objects.create(
            date_end=date_end, date_start=date_start, name="2023/2024", order=1, short_name="23/24", start_year=2023
        )
        str_ = scholar_year.__str__()
        self.assertEqual(str_, scholar_year.name)

    def test_to_dict(self):
        date_start = datetime.datetime.now()
        date_end = datetime.datetime.now()
        scholar_year = ScholarYear.objects.create(
            created_by=self.admin, date_end=date_end, date_start=date_start, name="2023/2024", order=1, short_name="23/24", start_year=2023
        )
        object_dict = scholar_year.to_dict()
        created_at = object_dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = object_dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(len(object_dict.keys()), 13)
        self.assertEqual(object_dict["created_by_id"], self.admin.id)
        self.assertEqual(object_dict["date_end"], date_end)
        self.assertEqual(object_dict["date_start"], date_start)
        self.assertEqual(object_dict["id"], scholar_year.id)
        self.assertEqual(object_dict["name"], scholar_year.name)
        self.assertEqual(object_dict["order"], scholar_year.order)
        self.assertFalse(object_dict["is_current"])
        self.assertFalse(object_dict["is_deleted"])
        self.assertTrue(created_at_test)
        self.assertTrue(object_dict["is_active"])
        self.assertTrue(last_update_at_test)

    def test_unique_scholar_year(self):
        date_start = datetime.datetime.now()
        date_end = datetime.datetime.now()
        ScholarYear.objects.create(
            created_by=self.admin, date_end=date_end, date_start=date_start, name="2023/2024", order=1,
            short_name="23/24", start_year=2023
        )
        with self.assertRaises(IntegrityError) as name_context:
            ScholarYear.objects.create(
                created_by=self.admin, date_end=date_end, date_start=date_start, name="2023/2024", order=2,
                short_name="23/24_", start_year=2024
            )
        self.assertIn('UNIQUE constraint failed', str(name_context.exception))
        transaction.set_rollback(False)
        with self.assertRaises(IntegrityError) as order_context:
            ScholarYear.objects.create(
                created_by=self.admin, date_end=date_end, date_start=date_start, name="2023/2024_", order=1,
                short_name="23/24_", start_year=2024
            )
        self.assertIn('UNIQUE constraint failed', str(order_context.exception))
        transaction.set_rollback(False)
        with self.assertRaises(IntegrityError) as short_name_context:
            ScholarYear.objects.create(
                created_by=self.admin, date_end=date_end, date_start=date_start, name="2023/2024_", order=2,
                short_name="23/24", start_year=2024
            )
        self.assertIn('UNIQUE constraint failed', str(short_name_context.exception))
        transaction.set_rollback(False)
        with self.assertRaises(IntegrityError) as start_year_context:
            ScholarYear.objects.create(
                created_by=self.admin, date_end=date_end, date_start=date_start, name="2023/2024_", order=2,
                short_name="23/24_", start_year=2023
            )
        self.assertIn('UNIQUE constraint failed', str(start_year_context.exception))
        transaction.set_rollback(True)
