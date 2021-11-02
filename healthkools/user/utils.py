from .models import User


def get_user_by_email_or_username(email_or_username):
    try:
        if "@" in email_or_username:
            user = User.objects.get(email=email_or_username)
        else:
            user = User.objects.get(username=email_or_username)
        return user
    except User.DoesNotExist:
        return "not_exists"
    except:
        return None
