from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.api.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
