# -*- coding: utf-8 -*-

from .models import *
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
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
