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


class TestSurveyResponseView:
    def test_post(self, client_authenticated, surveys):
        data = {
            "survey": surveys[0].id,
            "response": '{"question1": "answer1", "question2": "answer2"}',
        }
        response = client_authenticated.post(
            reverse("api:survey:surveyresponse-list"),
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["survey"] == surveys[0].id
        assert response.data["response"] == data["response"]
