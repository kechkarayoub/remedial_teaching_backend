# -*- coding: utf-8 -*-

from .models import *
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _


class AccountTypeServiceModelTests(TestCase):

    def test_service_name(self):
        account_type_service_1 = AccountTypeService()
        account_type_service_2 = AccountTypeService(service="hospital")
        self.assertEqual(account_type_service_1.service_name, _("Other"))
        self.assertEqual(account_type_service_2.service_name, _("Hospital"))

    def test_type_name(self):
        account_type_service_1 = AccountTypeService()
        account_type_service_2 = AccountTypeService(type="director")
        self.assertEqual(account_type_service_1.type_name, _("Other"))
        self.assertEqual(account_type_service_2.type_name, _("Director"))

    def test_to_dict(self):
        account_type_service = AccountTypeService(service="hospital", type="director")
        account_type_service.save()
        dict = account_type_service.to_dict()
        self.assertEqual(dict["id"], 1)
        self.assertEqual(dict["service"], "hospital")
        self.assertEqual(dict["service_name"], _("Hospital"))
        self.assertEqual(dict["type"], "director")
        self.assertEqual(dict["type_name"], _("Director"))


class UserModelTests(TestCase):

    def test_accounts_types_services_relations_are_empty(self):
        """
        accounts_types_services are empty by default.
        """
        user = User(username="test_username")
        user.save()
        self.assertIs(user.accounts_types_services.filter().exists(), False)

    def test_add_account_type_service(self):
        user = User(username="test_username")
        user.save()
        account_type_service = AccountTypeService(service="hospital", type="director")
        account_type_service.save()
        user.add_account_type_service(account_type_service)
        self.assertIs(user.accounts_types_services.filter().exists(), True)

    def test_to_dict(self):
        user = User(username="test_username", last_name="last_name")
        user.save()
        dict = user.to_dict()
        account_type_service = AccountTypeService(service="hospital", type="director")
        account_type_service.save()
        user.add_account_type_service(account_type_service)
        dict_2 = user.to_dict(get_accounts_types_services=True)
        self.assertEqual(dict["email_is_valid"], False)
        self.assertEqual(dict["first_name"], "")
        self.assertEqual(dict["id"], 1)
        self.assertEqual(dict["is_active"], True)
        self.assertEqual(dict["last_name"], "last_name")
        self.assertEqual(dict["phone"], None)
        self.assertEqual(dict["phone_is_valid"], False)
        self.assertEqual(dict["username"], "test_username")
        self.assertEqual(dict.get("accounts_types_services"), None)
        self.assertEqual(len(dict_2.get("accounts_types_services")), 1)
        self.assertEqual(dict_2.get("accounts_types_services")[0]['id'], 1)
        self.assertEqual(dict_2.get("accounts_types_services")[0]['service'], "hospital")
        self.assertEqual(dict_2.get("accounts_types_services")[0]['type'], "director")
