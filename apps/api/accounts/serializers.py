from allauth.account.utils import user_pk_to_url_str
from allauth.utils import build_absolute_uri
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from dj_rest_auth.serializers import (
    PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer,
)
from dj_rest_auth.serializers import (
    PasswordResetSerializer as DefaultPasswordResetSerializer,
)
from django.urls import reverse
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer


def default_url_generator(request, user, temp_key):
    path = reverse(
        "accounts:password_reset_confirm",
        args=[user_pk_to_url_str(user), temp_key],
    )

    if api_settings.PASSWORD_RESET_USE_SITES_DOMAIN:
        url = build_absolute_uri(None, path)
    else:
        url = build_absolute_uri(request, path)

    url = url.replace("%3F", "?")

    return url


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["user_id"] = user.id

        return token


class LoginSerializer(BaseLoginSerializer):
    username = None


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token": "Token is blacklisted",
        "no_token": "Token is required",
    }


class PasswordResetSerializer(DefaultPasswordResetSerializer):
    def get_email_options(self):
        return {
            "url_generator": default_url_generator,
        }


class PasswordResetConfirmSerializer(DefaultPasswordResetConfirmSerializer):
    pass


class RegisterSerializer(BaseRegisterSerializer):
    """
    Custom RegisterSerializer that handles phone field in Profile model
    """

    phone = PhoneNumberField(required=False, allow_blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the required attribute that dj-rest-auth expects
        self._has_phone_field = True

    def custom_signup(self, request, user):
        """
        Create user profile with phone number if provided
        """
        from apps.users.models import Profile

        phone = self.validated_data.get("phone")

        # Get or create profile
        profile, created = Profile.objects.get_or_create(user=user)

        # Update phone if provided
        if phone:
            profile.phone = phone
            profile.save()
