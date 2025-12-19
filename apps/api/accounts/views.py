from dj_rest_auth.views import LoginView as DefaultLoginView
from dj_rest_auth.views import PasswordChangeView as DefaultPasswordChangeView
from dj_rest_auth.views import PasswordResetConfirmView as DefaultPasswordResetConfirmView
from dj_rest_auth.views import PasswordResetView as DefaultPasswordResetView
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView

User = get_user_model()


class LoginView(DefaultLoginView):
    pass


class LogoutView(DefaultLoginView):
    allowed_methods = ["POST"]
    # serializer_class = None


class PasswordChangeView(DefaultPasswordChangeView):
    pass


class PasswordResetView(DefaultPasswordResetView):
    pass


class PasswordResetConfirmView(DefaultPasswordResetConfirmView):
    pass


class UserDetailsView(RetrieveUpdateAPIView):
    from apps.api.users.serializers import UserDetailSerializer

    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.all()
