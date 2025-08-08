from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BusinessPartner, DeliveryRequest, DeliveryPartner
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # generate the default token response

        # Add custom fields
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "business_name": self.user.partner_profile.business_name,
            "address": self.user.partner_profile.address,
            "groups": list(self.user.groups.values_list("name", flat=True)),
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "email"]


class BusinessPartnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    business_name = serializers.CharField(max_length=200, required=False)
    address = serializers.CharField(max_length=100, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = BusinessPartner
        fields = ["id", "user", "business_name", "address", "created_at", "updated_at"]

    def validate_user(self, value):
        username = value.get("username")

        if not username:
            raise serializers.ValidationError("Username is required.")

        if username.isdigit() or username.isalpha():
            raise serializers.ValidationError("Username must be alphanumeric.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists.")

        return value

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
