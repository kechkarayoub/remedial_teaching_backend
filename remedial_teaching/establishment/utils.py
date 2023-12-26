# -*- coding: utf-8 -*-

from .models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import activate, gettext_lazy as _
import after_response
import html2text
import logging

logger = logging.getLogger("django")


