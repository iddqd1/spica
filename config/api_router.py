from django.conf import settings
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from spica.users.api.views import CreateUserViewSet
from spica.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("users-create", CreateUserViewSet, basename="users-create")


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("", include("survey.urls", namespace="survey")),
]
