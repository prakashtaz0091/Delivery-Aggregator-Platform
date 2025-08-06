from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    "delivery-requests", views.DeliveryRequestView, basename="delivery-requests"
)


urlpatterns = [
    path(
        "register-business-partner/",
        views.BusinessPartnerRegisterView.as_view(),
        name="register-business-partner",
    ),
] + router.urls
