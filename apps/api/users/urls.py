from rest_framework import routers

from apps.api.users.views import UserViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = []

urlpatterns += router.urls
