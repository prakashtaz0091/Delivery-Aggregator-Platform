from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BusinessPartner


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "password", "last_name", "email"]


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
