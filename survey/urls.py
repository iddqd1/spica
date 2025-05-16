from rest_framework import routers

from survey import views

app_name = "survey"

router = routers.SimpleRouter()
router.register(r"surveys", views.SurveyViewSet)
router.register(
    r"surveys-response",
    views.SurveyResponseViewSet,
    basename="surveyresponse",
)
urlpatterns = router.urls
