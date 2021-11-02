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

    def test_get_security_questions(self):
        user = User(username="test_username")
        user.save()
        user_security_question = UserSecurityQuestion(security_question="what_is_your_birthday", user=user, response="birthday")
        user_security_question2 = UserSecurityQuestion(security_question="what_is_your_favorite_car", user=user, response="car")
        user_security_question.save()
        user_security_question2.save()
        user_security_questions = user.get_security_questions()
        self.assertEqual(len(user_security_questions), 2)
        self.assertEqual(user_security_questions[0], user_security_question.to_dict())
        self.assertEqual(user_security_questions[1], user_security_question2.to_dict())

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
        user = User(username="test_username", last_name="last_name", gender="m")
        user.save()
        dict = user.to_dict()
        account_type_service = AccountTypeService(service="hospital", type="director")
        account_type_service.save()
        user.add_account_type_service([account_type_service])
        dict_2 = user.to_dict(get_accounts_types_services=True)
        self.assertEqual(dict["country_code"], "")
        self.assertEqual(dict["email_is_validated"], False)
        self.assertEqual(dict["first_name"], "")
        self.assertEqual(dict["gender"], "m")
        self.assertEqual(dict["id"], 1)
        self.assertEqual(dict["is_active"], True)
        self.assertEqual(dict["language"], "fr")
        self.assertEqual(dict["language_name"], _("French"))
        self.assertEqual(dict["last_name"], "last_name")
        self.assertEqual(dict["phone"], None)
        self.assertEqual(dict["phone_is_valid"], False)
        self.assertEqual(dict["phone_is_validated"], False)
        self.assertEqual(dict["username"], "test_username")
        self.assertEqual(dict.get("accounts_types_services"), None)
        self.assertEqual(len(dict_2.get("accounts_types_services")), 1)
        self.assertEqual(dict_2.get("accounts_types_services")[0]['id'], 1)
        self.assertEqual(dict_2.get("accounts_types_services")[0]['service'], "hospital")
        self.assertEqual(dict_2.get("accounts_types_services")[0]['type'], "director")


class UserSecurityQuestionModelTests(TestCase):

    def test_to_dict(self):
        credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        user = User.objects.create_user(**credentials)
        user_security_question = UserSecurityQuestion(security_question="what_is_your_birthday", user=user)
        user_security_question.save()
        dict = user_security_question.to_dict()
        self.assertEqual(dict["id"], 1)
        self.assertEqual(dict["response"], "")
        self.assertEqual(dict["security_question"], "what_is_your_birthday")

    def test_get_list_choices(self):
        list_choices = UserSecurityQuestion.get_list_choices()
        self.assertEqual(list_choices, UserSecurityQuestion.SECURITY_QUESTIONS_LIST)


class LogInTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)

    def test_login_success(self):
        response = self.client.post('/user/login_with_token/', {
            'email_or_username': 'testuser',
            'password': 'secret'
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(json_response.get("user").get("username"), 'testuser')
        self.assertIs(json_response.get("access_token") is None, False)
        self.assertEqual(len(json_response.keys()), 3)
        self.assertEqual(len(json_response.get("user").keys()), 15)

    def test_login_failed(self):
        response1 = self.client.post('/user/login_with_token/', {'email_or_username': 'testusers', 'password': 'secret'}, follow=True)
        json_response1 = json.loads(response1.content)
        response2 = self.client.post('/user/login_with_token/', {'email_or_username': 'testuser', 'password': 'secrets'}, follow=True)
        json_response2 = json.loads(response2.content)
        response3 = self.client.post('/user/login_with_token/', {'username': 'testuser', 'password': 'secrets'}, follow=True)
        json_response3 = json.loads(response3.content)
        self.assertFalse(json_response1.get("success"))
        self.assertEqual(_(json_response1.get("message")), _('Invalid credentials!'))
        self.assertIs(json_response1.get("access_token") is None, True)
        self.assertFalse(json_response2.get("success"))
        self.assertEqual(_(json_response2.get("message")), _('Invalid credentials!'))
        self.assertIs(json_response2.get("access_token") is None, True)
        self.assertEqual(_(json_response3.get("message")), _('An error occurred when log in!'))
        self.assertIs(json_response3.get("access_token") is None, True)


class ViewTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'email': 'testemail@example.com',
            'password': 'secret',
            'email_is_validated': True,
        }
        User.objects.create_user(**self.credentials)

    def test_check_if_email_or_username_exists(self):
        email = 'testemail@example.com'
        username = 'testuser'
        data = {
            "email_or_username": "no_exists@example.com",
        }
        response = self.client.get('/user/check_if_email_or_username_exists', data, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("user_exists"))
        self.assertEqual(json_response.get("message"), '')
        data = {
            "email_or_username": "no_exists",
        }
        response = self.client.get('/user/check_if_email_or_username_exists', data, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("user_exists"))
        self.assertEqual(json_response.get("message"), '')
        data = {
            "email_or_username": email,
            "current_language": "en",
        }
        response = self.client.get('/user/check_if_email_or_username_exists', data, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("user_exists"))
        self.assertEqual(json_response.get("message"), _("The email: {} already exists!").format(email))
        data = {
            "email_or_username": username,
            "current_language": "en",
        }
        response = self.client.get('/user/check_if_email_or_username_exists', data, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("user_exists"))
        self.assertEqual(json_response.get("message"), _("The username: {} already exists!").format(username))
