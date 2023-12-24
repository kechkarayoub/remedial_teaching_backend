# -*- coding: utf-8 -*-

from .models import *
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from unittest.mock import patch
from user.models import Establishment
import json, datetime
from datetime import timezone


class HomeViewsTest(TestCase):

    def setUp(self):
        pass

    def test_general_information_api(self):
        response = self.client.get('/general_information_api', {}, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(json_response.get("general_information").get("site_name"), settings.SITE_NAME)
        self.assertEqual(json_response.get("general_information").get("contact_email"), settings.CONTACT_EMAIL)
        self.assertEqual(len(json_response.get("general_information").keys()), 2)

    def test_services_accounts_types_api(self):
        response = self.client.get('/services_accounts_types_api', {}, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(len(json_response.get("services_accounts_types")), len(Establishment.TYPES_DICT.keys()))

