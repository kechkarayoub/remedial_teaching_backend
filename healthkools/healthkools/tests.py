# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import json


class HealthKoolsViewsTest(TestCase):

    def setUp(self):
        pass

    def test_general_information_api(self):
        response = self.client.get('/general_information_api', {}, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(json_response.get("general_information").get("site_name"), settings.SITE_NAME)
        self.assertEqual(json_response.get("general_information").get("contact_email"), settings.CONTACT_EMAIL)
        self.assertEqual(len(json_response.get("general_information").keys()), 2)
