from factory import fuzzy
from factory.django import DjangoModelFactory

from survey import models


class SurveyFactory(DjangoModelFactory[models.Survey]):
    title = fuzzy.FuzzyText(length=20)
    description = fuzzy.FuzzyText(length=100)
    configuration = fuzzy.FuzzyText(length=4000)

    class Meta:
        model = models.Survey
        django_get_or_create = ["title"]
