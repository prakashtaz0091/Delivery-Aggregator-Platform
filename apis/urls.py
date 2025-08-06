from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    "delivery-requests", views.DeliveryRequestView, basename="delivery-requests"
)
router.register(
    "delivery-partners", views.DeliveryPartnerView, basename="delivery-partners"
)

urlpatterns = [
    path(
        "register-business-partner/",
        views.BusinessPartnerRegisterView.as_view(),
        name="register-business-partner",
    ),
] + router.urls
