from rest_framework import routers

from payment import views

app_name = "payment"

router = routers.SimpleRouter()
router.register(r"stripe-checkout", views.StripePaymentView, basename="stripe-checkout")

urlpatterns = router.urls
