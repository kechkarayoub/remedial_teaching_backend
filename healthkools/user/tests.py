# -*- coding: utf-8 -*-
import datetime
from django.core import mail
from django.conf import settings
from .models import *
from .utils import contact_new_user, get_user_by_email_or_username
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
import json
import os


class EstablishmentModelTests(TestCase):

    def test___str__(self):
        establishment = Establishment(name="Hospital1")
        establishment.save()
        str_ = establishment.__str__()
        self.assertEqual(str_, establishment.type_name + "_" + establishment.name)

    def test_type_name(self):
        establishment = Establishment(name="Hospital1")
        establishment.save()
        establishment2 = Establishment(name="Hospital2", type="hospital")
        establishment2.save()
        establishment3 = Establishment(name="Laboratory1", type="laboratory")
        establishment3.save()
        self.assertEqual(establishment.type_name, _("Hospital"))
        self.assertEqual(establishment2.type_name, _("Hospital"))
        self.assertEqual(establishment3.type_name, _("Laboratory"))

    def test_to_dict(self):
        establishment = Establishment(
            address="address", address_ar="address_ar", city="city", email="email@yopmail.com", fax="+212522xxxxxx",
            fax_is_valid=True, logo_url="logo_url", name="name", name_ar="name_ar", type="laboratory",
            website_url="localhost"
        )
        establishment.save()
        dict = establishment.to_dict()
        created_at = dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(dict["address"], "address")
        self.assertEqual(dict["address_ar"], "address_ar")
        self.assertEqual(dict["city"], "city")
        self.assertEqual(dict["email"], "email@yopmail.com")
        self.assertEqual(dict["fax"], "+212522xxxxxx")
        self.assertEqual(dict["fax_is_valid"], True)
        self.assertEqual(dict["fax_is_validated"], False)
        self.assertEqual(dict["id"], 1)
        self.assertEqual(dict["logo_url"], "logo_url")
        self.assertEqual(dict["mobile_phone"], None)
        self.assertEqual(dict["mobile_phone_is_valid"], False)
        self.assertEqual(dict["mobile_phone_is_validated"], False)
        self.assertEqual(dict["name"], "name")
        self.assertEqual(dict["name_ar"], "name_ar")
        self.assertEqual(dict["phone"], None)
        self.assertEqual(dict["phone_is_valid"], False)
        self.assertEqual(dict["phone_is_validated"], False)
        self.assertEqual(dict["phone2"], None)
        self.assertEqual(dict["phone2_is_valid"], False)
        self.assertEqual(dict["phone2_is_validated"], False)
        self.assertEqual(dict["type"], "laboratory")
        self.assertEqual(dict["type_name"], _("Laboratory"))
        self.assertEqual(dict["website_url"], "localhost")
        self.assertEqual(len(dict.keys()), 27)
        self.assertFalse(dict["is_deleted"])
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(dict["is_active"])


class UserModelTests(TestCase):

    def test_language_name(self):
        user = User(username="test_username")
        user.save()
        user2 = User(username="test_username2", language="ar")
        user2.save()
        self.assertEqual(user.language_name, _("French"))
        self.assertEqual(user2.language_name, _("Arabic"))

    def test_to_dict(self):
        user = User(username="test_username", last_name="last_name", gender="m")
        user.save()
        dict = user.to_dict()
        created_at = dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(dict["address"], "")
        self.assertIsNone(dict["birthday"])
        self.assertEqual(dict["country_code"], "")
        self.assertEqual(dict["country_name"], "")
        self.assertEqual(dict["email_is_validated"], False)
        self.assertEqual(dict["first_name"], "")
        self.assertEqual(dict["gender"], "m")
        self.assertEqual(dict["image_url"], "")
        self.assertEqual(dict["id"], 1)
        self.assertEqual(dict["language"], "fr")
        self.assertEqual(dict["language_name"], _("French"))
        self.assertEqual(dict["last_name"], "last_name")
        self.assertEqual(dict["mobile_phone"], None)
        self.assertEqual(dict["mobile_phone_is_valid"], False)
        self.assertEqual(dict["mobile_phone_is_validated"], False)
        self.assertEqual(dict["username"], "test_username")
        self.assertEqual(len(dict.keys()), 21)
        self.assertFalse(dict["is_deleted"])
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(dict["is_active"])

    def test___str__(self):
        user = User(username="test_username", last_name="last_name", gender="m")
        user.save()
        str_ = user.__str__()
        self.assertEqual(str_, "test_username")


class EstablishmentUserModelTests(TestCase):

    def test___str__(self):
        hospital = Establishment.objects.create(name="Hospital", type="hospital")
        user = User.objects.create(username="test_username", last_name="last_name", first_name="first_name")
        establishment_user = EstablishmentUser(establishment=hospital, user=user)
        establishment_user.save()
        str_ = establishment_user.__str__()
        self.assertEqual(str_, "1")

    def test_to_dict(self):
        hospital = Establishment.objects.create(name="Hospital", type="hospital")
        user = User.objects.create(username="test_username", last_name="last_name", first_name="first_name")
        establishment_user = EstablishmentUser(
            establishment=hospital, user=user, account_type="_assistant_", is_accepted=True, first_name="first_name",
            last_name="last_name",
        )
        establishment_user.save()
        dict = establishment_user.to_dict()
        created_at = dict["created_at"]
        created_at_test = created_at - datetime.timedelta(seconds=5) <= created_at <= created_at + datetime.timedelta(seconds=5)
        last_update_at = dict["last_update_at"]
        last_update_at_test = last_update_at - datetime.timedelta(seconds=5) <= last_update_at <= last_update_at + datetime.timedelta(seconds=5)
        self.assertEqual(dict["address"], "")
        self.assertIsNone(dict["birthday"])
        self.assertEqual(dict["country_code"], "")
        self.assertEqual(dict["country_name"], "")
        self.assertEqual(dict["email_is_accepted"], False)
        self.assertEqual(dict["establishment_id"], 1)
        self.assertEqual(dict["first_name"], "first_name")
        self.assertEqual(dict["gender"], "")
        self.assertEqual(dict["id"], 1)
        self.assertEqual(dict["image_url"], "")
        self.assertEqual(dict["is_accepted"], True)
        self.assertEqual(dict["last_name"], "last_name")
        self.assertEqual(dict["mobile_phone"], None)
        self.assertEqual(dict["mobile_phone_is_valid"], False)
        self.assertEqual(dict["mobile_phone_is_accepted"], False)
        self.assertEqual(dict["user_id"], 1)
        self.assertEqual(len(dict.keys()), 21)
        self.assertFalse(dict["is_deleted"])
        self.assertTrue(last_update_at_test)
        self.assertTrue(created_at_test)
        self.assertTrue(dict["is_active"])


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

    def test___str__(self):
        user = User.objects.get(email="testemail@example.com")
        user_email_confirmation_key = UserEmailConfirmationKey.create(user)
        str_ = user_email_confirmation_key.__str__()
        self.assertEqual(str_, user.__str__() + "_" + user_email_confirmation_key.key)


class LogInTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
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
        self.assertEqual(len(json_response.get("user").keys()), 21)

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
            'mobile_phone_is_valid': False,
            'mobile_phone': "+212645454545",
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
        self.assertEqual(user.mobile_phone_is_valid, False)
        self.assertIs(user.check_password("password") is True, True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "حسابك {site_name}".format(site_name=settings.SITE_NAME))
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
            'mobile_phone_is_valid': False,
            'mobile_phone': "+212645454545",
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
            'mobile_phone_is_valid': False,
            'mobile_phone': "+212645454545",
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
            'mobile_phone': "+212645454545",
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
        response = self.client.post('/user/register/', {
            'username': 'raise_exception',
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("success"))
        self.assertEqual(json_response.get("message"), "Une erreur s'est produite lors de la vérification du nom d'utilisateur !")
        response = self.client.post('/user/register/', {
            'email': 'raise_exception',
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertFalse(json_response.get("success"))
        self.assertEqual(json_response.get("message"), "Une erreur s'est produite lors de la vérification de l'e-mails !")


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
            'mobile_phone_is_valid': False,
            'mobile_phone': "+212645454545",
            'username': "username",
        }, follow=True)
        user = User.objects.get(username="username")
        ueck2 = UserEmailConfirmationKey.create(user=user)
        ueck2.creation_time = ueck2.creation_time.replace(year=ueck2.creation_time.year - 2)
        ueck2.save()
        response = self.client.post('/user/resend_activation_email/', {
            'current_language': 'en',
            'username': "username",
        }, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(len(json_response.keys()), 2)
        self.assertEqual(json_response.get("message"), "A new activation email is sent to the address email@email.com.")
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, "حسابك {site_name}".format(site_name=settings.SITE_NAME))
        self.assertIn("last_name first_name", mail.outbox[1].body)
        user.my_email_confirmation_keys.filter().delete()
        user.email_is_validated = False
        user.save()
        response2 = self.client.post('/user/resend_activation_email/', {
            'current_language': 'en',
            'username': "username",
        }, follow=True)
        json_response2 = json.loads(response2.content)
        self.assertTrue(json_response2.get("success"))
        self.assertEqual(len(json_response2.keys()), 2)
        self.assertEqual(json_response2.get("message"), "A new activation email is sent to the address email@email.com.")
        self.assertEqual(len(mail.outbox), 3)
        self.assertEqual(mail.outbox[2].subject, "حسابك {site_name}".format(site_name=settings.SITE_NAME))
        self.assertIn("last_name first_name", mail.outbox[2].body)
        response3 = self.client.post('/user/resend_activation_email/', {
            'current_language': 'en',
            'username': "username",
        }, follow=True)

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
            'mobile_phone_is_valid': False,
            'mobile_phone': "+212645454545",
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
        response3 = self.client.post('/user/resend_activation_email/', {
            'current_language': 'en',
            'username': "raise_exception",
        }, follow=True)
        json_response3 = json.loads(response3.content)
        self.assertFalse(json_response3.get("success"))
        self.assertEqual(json_response3.get("message"), "An error occurred when checking username!")



class ViewTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser2',
            'email': 'testemail@example.com',
            'first_name': 'first_name2',
            'last_name': 'last_name',
            'password': 'secret',
            'email_is_validated': True,
        }
        User.objects.create_user(**self.credentials)

    def test_check_if_email_or_username_exists(self):
        email = 'testemail@example.com'
        username = 'testuser2'
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
        user = User.objects.get(username="testuser2")
        user.language = "ar"
        user.save()
        user_email_confirmation_key = UserEmailConfirmationKey.create(user)
        contact_new_user(user, user_email_confirmation_key.key)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "حسابك {site_name}".format(site_name=settings.SITE_NAME))
        self.assertIn(user.last_name + " " + user.first_name, mail.outbox[0].body)
        with self.settings(EMAIL_SMTP_PROVIDER=''):
            contact_new_user(user, user_email_confirmation_key.key)
            lines = open(os.path.join(settings.BASE_DIR, 'log/main_log_test.log'))
            lines_target = [(line + "") for line in lines if line and ']: You should configure a smtp email provider' in line]
            line_target = lines_target[0] if lines_target else ""
            self.assertNotEqual(line_target, "")
            self.assertIn("]: You should configure a smtp email provider", line_target)
            datetime_test = datetime.datetime.now().strftime("%Y-%m-%d %H:")
            self.assertIn(datetime_test, line_target)
            self.assertIn("- WARNING - utils - utils.py -", line_target)

    def test_get_user_by_email_or_username(self):
        user1 = get_user_by_email_or_username("testuser2")
        user2 = get_user_by_email_or_username("testemail@example.com")
        user3 = get_user_by_email_or_username("testema005il@example.com")
        self.assertEqual(user1.email, "testemail@example.com")
        self.assertEqual(user2.username, "testuser2")
        self.assertEqual(user3, "not_exists")
