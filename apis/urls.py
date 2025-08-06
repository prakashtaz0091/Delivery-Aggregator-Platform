from django.urls import path
from .views import BusinessPartnerRegisterView

urlpatterns = [
    path(
        "register-business-partner/",
        BusinessPartnerRegisterView.as_view(),
        name="register-business-partner",
    ),
]
