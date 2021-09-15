# -*- coding: utf-8 -*-

from .models import *
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
import json


class AccountTypeServiceModelTests(TestCase):

    def test_service_name(self):
        account_type_service_1 = AccountTypeService()
        account_type_service_2 = AccountTypeService(service="hospital")
        account_type_service_3 = AccountTypeService(service="ascdrf")
        self.assertEqual(account_type_service_1.service_name, _("Other"))
        self.assertEqual(account_type_service_2.service_name, _("Hospital"))
        self.assertEqual(account_type_service_3.service_name, "---")

    def test_type_name(self):
        account_type_service_1 = AccountTypeService()
        account_type_service_2 = AccountTypeService(type="director")
        account_type_service_3 = AccountTypeService(type="gjyukj")
        self.assertEqual(account_type_service_1.type_name, _("Other"))
        self.assertEqual(account_type_service_2.type_name, _("Director"))
        self.assertEqual(account_type_service_3.type_name, "---")

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
        user.add_account_type_service([account_type_service])
        self.assertIs(user.accounts_types_services.filter().exists(), True)

    def test_add_account_type_service_with_ids(self):
        user = User(username="test_username")
        user.save()
        account_type_service = AccountTypeService(service="hospital", type="director")
        account_type_service.save()
        user.add_account_type_service(ids=[account_type_service.id])
        self.assertIs(user.accounts_types_services.filter().exists(), True)

    def test_language_name(self):
        user = User(username="test_username")
        user.save()
        user2 = User(username="test_username2", language="ar")
        user2.save()
        self.assertEqual(user.language_name, _("French"))
        self.assertEqual(user2.language_name, _("Arabic"))

    def test_remove_account_type_service(self):
        user = User(username="test_username")
        user.save()
        account_type_service = AccountTypeService(service="hospital", type="director")
        account_type_service.save()
        user.add_account_type_service([account_type_service])
        self.assertIs(user.accounts_types_services.filter().exists(), True)
        user.remove_account_type_service([account_type_service])
        self.assertIs(user.accounts_types_services.filter().exists(), False)

    def test_remove_account_type_service_with_ids(self):
        user = User(username="test_username")
        user.save()
        account_type_service = AccountTypeService(service="hospital", type="director")
        account_type_service.save()
        user.add_account_type_service([account_type_service])
        self.assertIs(user.accounts_types_services.filter().exists(), True)
        user.remove_account_type_service(ids=[account_type_service.id])
        self.assertIs(user.accounts_types_services.filter().exists(), False)

    def test_to_dict(self):
        user = User(username="test_username", last_name="last_name")
        user.save()
        dict = user.to_dict()
        account_type_service = AccountTypeService(service="hospital", type="director")
        account_type_service.save()
        user.add_account_type_service([account_type_service])
        dict_2 = user.to_dict(get_accounts_types_services=True)
        self.assertEqual(dict["email_is_valid"], False)
        self.assertEqual(dict["first_name"], "")
        self.assertEqual(dict["id"], 1)
        self.assertEqual(dict["is_active"], True)
        self.assertEqual(dict["language"], "fr")
        self.assertEqual(dict["language_name"], _("French"))
        self.assertEqual(dict["last_name"], "last_name")
        self.assertEqual(dict["phone"], None)
        self.assertEqual(dict["phone_is_valid"], False)
        self.assertEqual(dict["username"], "test_username")
        self.assertEqual(dict.get("accounts_types_services"), None)
        self.assertEqual(len(dict_2.get("accounts_types_services")), 1)
        self.assertEqual(dict_2.get("accounts_types_services")[0]['id'], 1)
        self.assertEqual(dict_2.get("accounts_types_services")[0]['service'], "hospital")
        self.assertEqual(dict_2.get("accounts_types_services")[0]['type'], "director")


class LogInTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)

    def test_login_success(self):
        response = self.client.post('/user/login_with_token/', self.credentials, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(json_response.get("user").get("username"), 'testuser')
        self.assertIs(json_response.get("access_token") is None, False)

    def test_login_failed(self):
        response1 = self.client.post('/user/login_with_token/', {'username': 'testusers', 'password': 'secret'}, follow=True)
        json_response1 = json.loads(response1.content)
        response2 = self.client.post('/user/login_with_token/', {'username': 'testuser', 'password': 'secrets'}, follow=True)
        json_response2 = json.loads(response2.content)
        self.assertFalse(json_response1.get("success"))
        self.assertEqual(json_response1.get("message"), _('User not found!'))
        self.assertIs(json_response1.get("access_token") is None, True)
        self.assertFalse(json_response2.get("success"))
        self.assertEqual(json_response2.get("message"), _('Password incorrect!'))
        self.assertIs(json_response2.get("access_token") is None, True)