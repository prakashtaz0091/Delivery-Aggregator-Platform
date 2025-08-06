from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BusinessPartner, DeliveryRequest, DeliveryPartner


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "email"]


class BusinessPartnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BusinessPartner
        fields = ["id", "user", "business_name", "address", "created_at", "updated_at"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        business_partner = BusinessPartner.objects.create(user=user, **validated_data)
        return business_partner


class DevliveryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRequest
        fields = [
            "id",
            "description",
            "status",
            "requester",
            "receiver_address",
            "receiver_name",
            "created_at",
            "updated_at",
        ]


class DeliveryPartnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DeliveryPartner
        fields = ["id", "user", "company_name", "created_at", "updated_at"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        delivery_partner = DeliveryPartner.objects.create(user=user, **validated_data)
        return delivery_partner
