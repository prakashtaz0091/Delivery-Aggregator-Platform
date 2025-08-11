from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    BusinessPartnerSerializer,
    DevliveryRequestSerializer,
    DeliveryPartnerSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import DeliveryRequest, DeliveryPartner
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .permissions import RoleBasedPermission


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class BusinessPartnerRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BusinessPartnerSerializer,
        examples=[
            OpenApiExample(
                name="Example Payload",
                value={
                    "user": {
                        "username": "prakash123",
                        "email": "prakash@example.com",
                        "password": "securepassword123",
                        "first_name": "Prakash",
                        "last_name": "Shrestha",
                    },
                    "business_name": "Optional",
                    "address": "Optional",
                },
                request_only=True,
                response_only=False,
            ),
        ],
        summary="Register a new business partner",
        description="This endpoint registers a new business partner along with their associated user account.",
    )
    def post(self, request):
        serializer = BusinessPartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Business partner registered successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryRequestView(ModelViewSet):
    model = DeliveryRequest
    serializer_class = DevliveryRequestSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:  # if use is admin/superuser
            return DeliveryRequest.objects.all()
        return DeliveryRequest.objects.filter(
            requester=self.request.user.partner_profile
        )


class DeliveryPartnerView(ModelViewSet):
    model = DeliveryPartner
    queryset = DeliveryPartner.objects.all()
    serializer_class = DeliveryPartnerSerializer
    permission_classes = [IsAuthenticated]
