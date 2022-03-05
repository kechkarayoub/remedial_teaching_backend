# -*- coding: utf-8 -*-

from .models import *
from django.http import JsonResponse
from django.utils.translation import activate, gettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from utils.utils import date_from_string
from .utils import get_user_by_email_or_username, contact_new_user
from django.conf import settings
import json


class LoginTokenView(APIView):
    def post(self, request, *args, **kwargs):
        """
            :param request: the user request
            :param args:
            :param kwargs:
            :return: return the user object representation and his token
        """
        email_or_username = request.data.get('email_or_username')
        password = request.data.get('password')
        selected_language = request.data.get('selected_language')
        if selected_language:
            activate(selected_language)
        user = get_user_by_email_or_username(email_or_username)
        if user == "not_exists":
            return JsonResponse({
                'success': False,
                'message': _('Invalid credentials!'),
            })
        elif user is None:
            return JsonResponse({
                'success': False,
                'message': _('An error occurred when log in!'),
            })
        request.session['language_id'] = user.language
        activate(user.language)
        if not user.check_password(password):
            return JsonResponse({
                'success': False,
                'message': _('Invalid credentials!'),
            })
        token, created = Token.objects.get_or_create(user=user)
        response = JsonResponse({
            'success': True,
            'access_token': token.key,
            'user': user.to_dict(),
        })
        response.set_cookie(key="jwt", value=token.key, httponly=True)
        return response


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        """
            :param request: the user request
            :param args:
            :param kwargs:
            :return: return a message confirmed that the account is created
        """
        address = request.data.get('address', '')
        birthday = date_from_string(request.data.get('birthday'))
        country_code = request.data.get('country_code', '')
        email = request.data.get('email', '')
        first_name = request.data.get('first_name', '')
        gender = request.data.get('gender', '')
        language = request.data.get('current_language', 'fr')
        last_name = request.data.get('last_name', '')
        password = request.data.get('password', '')
        phone_is_valid = request.data.get('is_valid_phone_number', False)
        phone = request.data.get('phone_number', '')
        username = request.data.get('username', '')
        if language:
            activate(language)
        try:
            User.objects.get(username=username)
            return JsonResponse({
                'success': False,
                'message': _('This username: {} is already exists!').format(username),
            })
        except User.DoesNotExist:
            try:
                User.objects.get(email=email)
                return JsonResponse({
                    'success': False,
                    'message': _('This email: {} is already exists!').format(email),
                })
            except User.DoesNotExist:
                pass
            except:
                return JsonResponse({
                    'success': False,
                    'message': _('An error occurred when checking email!'),
                })
        except:
            return JsonResponse({
                'success': False,
                'message': _('An error occurred when checking username!'),
            })
        errors = {}
        kwargs = {
            "address": address,
            "birthday": birthday,
            "country_code": country_code,
            "gender": gender,
            "language": language,
            "phone_is_valid": phone_is_valid,
            "phone": phone,
        }
        if email:
            kwargs["email"] = email
        else:
            errors["email"] = _('Email is required!')
        if first_name:
            kwargs["first_name"] = first_name
        else:
            errors["first_name"] = _('First name is required!')
        if last_name:
            kwargs["last_name"] = last_name
        else:
            errors["last_name"] = _('Last name is required!')
        if not password:
            errors["password"] = _('Password is required!')
        if username:
            kwargs["username"] = username
        else:
            errors["username"] = _('Username is required!')
        if errors.keys():
            return JsonResponse({
                'success': False,
                'errors': errors,
            })
        user = User.objects.create(**kwargs)
        user.set_password(password)
        user.save()
        user_email_confirmation_key = UserEmailConfirmationKey.create(user)
        request.session['language_id'] = user.language
        if settings.TEST_SETTINGS:
            contact_new_user(user, user_email_confirmation_key.key)
        else:
            contact_new_user.after_response(user, user_email_confirmation_key.key)
        # User.objects.filter(pk=user.id).delete()
        response = JsonResponse({
            'success': True,
            'messages': {
                "title": _("Your account is created."),
                "p1": _("An activation email is sent to the address {} for you to activate your email so that you can log in.").format(email),
                "p2": _("If you haven't received the email, click here to resend it."),
                "username": username,
            },
        })
        return response


class ResendActivationEmailView(APIView):
    def post(self, request, *args, **kwargs):
        """
            :param request: the user request
            :param args:
            :param kwargs:
            :return: return a message confirmed that the email activation is ressent
        """
        language = request.data.get('current_language', 'fr')
        username = request.data.get('username', '')
        if language:
            activate(language)
        try:
            user = User.objects.get(username=username)
            if user.email_is_validated:
                return JsonResponse({
                    'success': False,
                    'message1': _('Your email address is already validated!'),
                    'message2': _('You can now log in with your username/email and password.'),
                })
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': _("We couldn't find an account with that username: {}!").format(username),
            })
        except:
            return JsonResponse({
                'success': False,
                'message': _('An error occurred when checking username!'),
            })
        user_email_confirmation_key = None
        for ueck in user.my_email_confirmation_keys.filter():
            if not ueck.is_expired:
                user_email_confirmation_key = ueck
                break
        if user_email_confirmation_key is None:
            user_email_confirmation_key = UserEmailConfirmationKey.create(user)
        request.session['language_id'] = language
        if settings.TEST_SETTINGS:
            contact_new_user(user, user_email_confirmation_key.key)
        else:
            contact_new_user.after_response(user, user_email_confirmation_key.key)
        if language:
            activate(language)
        response = JsonResponse({
            'success': True,
            'message': _("A new activation email is sent to the address {}.").format(user.email),
        })
        return response


@api_view(['GET'])
def check_if_email_or_username_exists(request):
    """
        :param request: the request user
        :return: return a message indicated if the email or username exists or not
    """
    data = request.GET
    email_or_username = data.get("email_or_username")
    current_language = data.get("current_language") or 'fr'
    activate(current_language)
    message = ""
    user_exists = False
    if "@" in email_or_username and User.objects.filter(email=email_or_username, email_is_validated=True).exists():
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
