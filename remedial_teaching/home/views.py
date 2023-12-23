# -*- coding: utf-8 -*-

from .models import FeedsLanguage
from django.http import JsonResponse
from django.utils.translation import activate, gettext_lazy as _
from django.conf import settings
from user.models import Establishment, EstablishmentUser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import json


@api_view(['GET'])
def feeds_languages_api(request):
    """
        :param request: user request
        :return: all storred feeds as objects grouped by language
    """
    feeds_languages = {}
    for feeds_language in FeedsLanguage.objects.filter():
        # for each stored language feeds, we get items, and we add them to feeds_languages dictionary
        feeds_languages[feeds_language.language] = feeds_language.to_items_list()
    response = JsonResponse({
        "feeds_languages": feeds_languages,
        "success": True,
    })
    return response


@api_view(['GET'])
def general_information_api(request):
    """
        :param request: user request
        :return: general information of the website
    """
    response = JsonResponse({
        "general_information": {
            "site_name": settings.SITE_NAME,
            "contact_email": settings.CONTACT_EMAIL,
        },
        "success": True,
    })
    return response


@api_view(['GET'])
def services_accounts_types_api(request):
    """
        :param request: user request
        :return: services and their accounts types
    """
    account_types_by_service = {
        "hospital": ["assistant", "director",  "doctor", "nurse", "patient", "other"],
        "laboratory": ["assistant", "director",  "doctor", "technician", "patient", "other"],
    }
    services_types = Establishment.TYPES_DICT
    services_accounts_types = []
    for service_key, service_name in services_types.items():
        accounts_types = {}
        for account_type in account_types_by_service.get(service_key) or []:
            accounts_types[account_type] = EstablishmentUser.ACCOUNT_TYPES_DICT[account_type]
        service_accounts_types = {
            "key": service_key,
            "name": service_name,
            "accounts_types": accounts_types,
        }
        services_accounts_types.append(service_accounts_types)
    response = JsonResponse({
        "services_accounts_types": services_accounts_types,
        "success": True,
    })
    return response

