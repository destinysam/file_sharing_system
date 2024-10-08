from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

def get_refresh_token_for_user(user: User) -> RefreshToken:
    refresh = RefreshToken.for_user(user)
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
    return refresh



def get_login_token(request,user: User):
    refresh = get_refresh_token_for_user(user)
    data = {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "refresh_exp_at": refresh["exp"],
        "access_exp_at": refresh.access_token["exp"],
    }
    return data



def get_token_from_refresh_token(refresh_token: RefreshToken):
    refresh = RefreshToken(token=refresh_token)
    data = {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "refresh_exp_at": refresh["exp"],
        "access_exp_at": refresh.access_token["exp"],
    }
    return data
