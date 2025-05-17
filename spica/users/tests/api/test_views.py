import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from spica.users.api.views import UserViewSet
from spica.users.models import User


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore[call-arg, arg-type, misc]

        assert response.data == {
            "url": f"http://testserver/api/users/{user.pk}/",
            "name": user.name,
        }


@pytest.mark.django_db
class TestCreateUserSerializer:
    def test_create_user(self, client):
        data = {
            "name": "Test User",
            "email": "john.doe@example.com",
            "password": "password123",
            "password_confirm": "password123",
        }
        response = client.post(reverse("api:users-create-list"), data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
