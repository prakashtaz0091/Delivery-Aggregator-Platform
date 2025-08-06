from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BusinessPartnerSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


class BusinessPartnerRegisterView(APIView):
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
                    },
                    "business_name": "Tajpuriya Traders",
                    "address": "Kathmandu, Nepal",
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
