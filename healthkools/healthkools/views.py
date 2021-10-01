# -*- coding: utf-8 -*-

# from .models import *
import pdb

from django.http import JsonResponse
from django.utils.translation import activate, ugettext_lazy as _
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import json


@api_view(['GET'])
def general_information(request):
    response = JsonResponse({
        "general_information": {
            "site_name": settings.SITE_NAME,
            "contact_email": settings.CONTACT_EMAIL,
        },
        "success": True,
    })
    return response
