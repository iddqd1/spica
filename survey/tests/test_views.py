import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestSurveyView:
    def test_get(self, client_authenticated, surveys):
        response = client_authenticated.get(
            reverse("api:survey:survey-list"),
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(surveys)
