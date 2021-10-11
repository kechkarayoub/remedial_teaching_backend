# -*- coding: utf-8 -*-

from .models import *
from django.http import JsonResponse
from django.utils.translation import activate, ugettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
import json


class LoginTokenView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            request.session['language_id'] = user.language
            activate(user.language)
        except:
            return JsonResponse({
                'success': False,
                'message': _('User not found!'),
            })
        if not user.check_password(password):
            return JsonResponse({
                'success': False,
                'message': _('Password incorrect!'),
            })
        token, created = Token.objects.get_or_create(user=user)
        response = JsonResponse({
            'success': True,
            'access_token': token.key,
            'user': user.to_dict(),
        })
        response.set_cookie(key="jwt", value=token.key, httponly=True)
        return response


@api_view(['GET'])
def check_if_email_or_username_exists(request):
    data = request.GET
    email_or_username = data.get("email_or_username")
    current_language = data.get("current_language") or 'fr'
    activate(current_language)
    message = ""
    user_exists = False
    if "@" in email_or_username and User.objects.filter(email=email_or_username, email_is_valid=True).exists():
        user_exists = True
        message = _("The email: {} already exists!").format(email_or_username)
    elif User.objects.filter(username=email_or_username).exists():
        user_exists = True
        message = _("The username: {} already exists!").format(email_or_username)
    response = JsonResponse({
        "message": message,
        "user_exists": user_exists,
    })
    return response


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def users_test_api(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = json.loads(request.body or "{}")
    response = JsonResponse({
        "users": [user.to_dict() for user in User.objects.filter(is_active=True)]
    })
    return response
