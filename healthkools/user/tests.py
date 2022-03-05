# -*- coding: utf-8 -*-
import datetime
from django.core import mail
from django.conf import settings
from .models import *
from .utils import contact_new_user
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
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
        self.assertEqual(len(dict.keys()), 17)
        self.assertEqual(len(dict_2.keys()), 18)
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


class UserEmailConfirmationKeyModelTests(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'email': 'testemail@example.com',
            'first_name': 'first_name2',
            'last_name': 'last_name',
            'password': 'secret',
        }
        User.objects.create_user(**self.credentials)

    def test_create(self):
        user = User.objects.get(email="testemail@example.com")
        user_email_confirmation_key = UserEmailConfirmationKey.create(user)
        self.assertEqual(UserEmailConfirmationKey.objects.get(key=user_email_confirmation_key.key, user=user).id, user_email_confirmation_key.id)

    def test_is_expired_false(self):
        user = User.objects.get(email="testemail@example.com")
        user_email_confirmation_key = UserEmailConfirmationKey.create(user)
        self.assertFalse(user_email_confirmation_key.is_expired)

    def test_is_expired_true(self):
        user = User.objects.get(email="testemail@example.com")
        creation_time = datetime.datetime.now() - datetime.timedelta(minutes=settings.EMAIL_CONFIRMATION_KEY_EXPIRATION_MINUTES + 1)
        user_email_confirmation_key = UserEmailConfirmationKey.create(user)
        user_email_confirmation_key.creation_time = creation_time.astimezone()
        user_email_confirmation_key.save()
        self.assertTrue(user_email_confirmation_key.is_expired)


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
        self.assertEqual(len(json_response.get("user").keys()), 17)

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


class RegisterTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email': 'testuser@email.com',
        }
        User.objects.create_user(**self.credentials)

    def test_register_with_all_attributes_success(self):
        response = self.client.post('/user/register/', {
            'address': 'address',
            'birthday': datetime.datetime.today().strftime("%d/%m/%Y"),
            'country_code': "MA",
            'email': "email@email.com",
            'first_name': "first_name",
            'gender': "m",
            'current_language': "ar",
            'last_name': "last_name",
            'password': "password",
            'phone_is_valid': False,
            'phone': "+212645454545",
            'username': "username",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(len(json_response.keys()), 2)
        self.assertIs(json_response.get("messages") is None, False)
        self.assertEqual(len(json_response.get("messages").keys()), 4)
        self.assertEqual(json_response.get("messages").get('username'), "username")
        user = User.objects.get(username='username')
        self.assertEqual(user.address, 'address')
        self.assertEqual(user.birthday, datetime.datetime.today().date())
        self.assertEqual(user.country_code, "MA")
        self.assertEqual(user.email, "email@email.com")
        self.assertEqual(user.first_name, "first_name")
        self.assertEqual(user.gender, "m")
        self.assertEqual(user.language, "ar")
        self.assertEqual(user.last_name, "last_name")
        self.assertEqual(user.phone_is_valid, False)
        self.assertIs(user.check_password("password") is True, True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Votre compte {site_name}".format(site_name=settings.SITE_NAME))
        self.assertIn(user.last_name + " " + user.first_name, mail.outbox[0].body)

    def test_register_with_required_attribites_success(self):
        response = self.client.post('/user/register/', {
            'email': "email@email.com",
            'first_name': "first_name",
            'last_name': "last_name",
            'password': "password",
            'username': "username",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(len(json_response.keys()), 2)
        user = User.objects.get(username='username')
        self.assertEqual(user.language, "fr")
        self.assertIs(user.check_password("password") is True, True)

    def test_register_failed(self):
        response = self.client.post('/user/register/', {
            'address': 'address',
            'birthday': datetime.datetime.today(),
            'country_code': "MA",
            'email': "",
            'first_name': "",
            'gender': "m",
            'language': "ar",
            'last_name': "",
            'password': "",
            'phone_is_valid': False,
            'phone': "+212645454545",
            'username': "",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("success"))
        self.assertEqual(len(json_response.keys()), 2)
        self.assertEqual(len(json_response.get("errors").keys()), 5)
        self.assertTrue(all(elem in json_response.get("errors").keys() for elem in ["email", "first_name", "last_name", "password", "username"]))
        response = self.client.post('/user/register/', {
            'address': 'address',
            'birthday': datetime.datetime.today(),
            'country_code': "MA",
            'email': "",
            'first_name': "",
            'gender': "m",
            'language': "ar",
            'last_name': "",
            'password': "",
            'phone_is_valid': False,
            'phone': "+212645454545",
            'username': "username",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("success"))
        self.assertEqual(len(json_response.keys()), 2)
        self.assertEqual(len(json_response.get("errors").keys()), 4)
        self.assertTrue(all(elem in json_response.get("errors").keys() for elem in ["email", "first_name", "last_name", "password"]))
        response = self.client.post('/user/register/', {
            'address': 'address',
            'email': "",
            'phone': "+212645454545",
            'username': "testuser",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("success"))
        self.assertEqual(json_response.get("message"), "Ce nom d'utilisateur : testuser existe déjà!")
        response = self.client.post('/user/register/', {
            'email': "testuser@email.com",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("success"))
        self.assertEqual(json_response.get("message"), "Cet email : testuser@email.com existe déjà!")


class ResendActivationEmailViewTest(TestCase):

    def test_resend_activation_email_success(self):
        self.client.post('/user/register/', {
            'address': 'address',
            'birthday': datetime.datetime.today().strftime("%d/%m/%Y"),
            'country_code': "MA",
            'email': "email@email.com",
            'first_name': "first_name",
            'gender': "m",
            'current_language': "ar",
            'last_name': "last_name",
            'password': "password",
            'phone_is_valid': False,
            'phone': "+212645454545",
            'username': "username",
        }, follow=True)
        response = self.client.post('/user/resend_activation_email/', {
            'current_language': 'en',
            'username': "username",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(len(json_response.keys()), 2)
        self.assertEqual(json_response.get("message"), "A new activation email is sent to the address email@email.com.")
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, "Votre compte {site_name}".format(site_name=settings.SITE_NAME))
        self.assertIn("last_name first_name", mail.outbox[1].body)

    def test_resend_activation_email_failed(self):
        self.client.post('/user/register/', {
            'address': 'address',
            'birthday': datetime.datetime.today().strftime("%d/%m/%Y"),
            'country_code': "MA",
            'email': "email@email.com",
            'first_name': "first_name",
            'gender': "m",
            'current_language': "ar",
            'last_name': "last_name",
            'password': "password",
            'phone_is_valid': False,
            'phone': "+212645454545",
            'username': "username",
        }, follow=True)
        user = User.objects.get(username="username")
        user.email_is_validated = True
        user.save()
        response = self.client.post('/user/resend_activation_email/', {
            'current_language': 'en',
            'username': "username2",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("success"))
        self.assertEqual(len(json_response.keys()), 2)
        self.assertEqual(json_response.get("message"), "We couldn't find an account with that username: username2!")
        self.assertEqual(len(mail.outbox), 1)
        response2 = self.client.post('/user/resend_activation_email/', {
            'current_language': 'en',
            'username': "username",
        }, follow=True)
        json_response2 = json.loads(response2.content)
        self.assertFalse(json_response2.get("success"))
        self.assertEqual(len(json_response2.keys()), 3)
        self.assertEqual(json_response2.get("message1"), "Your email address is already validated!")
        self.assertEqual(json_response2.get("message2"), "You can now log in with your username/email and password.")
        self.assertEqual(len(mail.outbox), 1)



class ViewTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'email': 'testemail@example.com',
            'first_name': 'first_name2',
            'last_name': 'last_name',
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

    def test_contact_new_user(self):
        user = User.objects.get(username="testuser")
        user_email_confirmation_key = UserEmailConfirmationKey.create(user)
        contact_new_user(user, user_email_confirmation_key.key)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Votre compte {site_name}".format(site_name=settings.SITE_NAME))
        self.assertIn(user.last_name + " " + user.first_name, mail.outbox[0].body)
