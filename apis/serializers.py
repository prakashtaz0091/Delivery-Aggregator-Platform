from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BusinessPartner, DeliveryRequest, DeliveryPartner, Address
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "name", "latitude", "longitude"]


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
        }
        try:
            data["user"].update(
                {
                    "business_name": self.user.partner_profile.business_name,
                    "address": AddressSerializer(
                        self.user.partner_profile.addresses.all(), many=True
                    ).data,
                    "groups": list(self.user.groups.values_list("name", flat=True)),
                }
            )
        except Exception as e:
            print(e)

        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "email"]


class BusinessPartnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    business_name = serializers.CharField(max_length=200, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = BusinessPartner
        fields = [
            "id",
            "user",
            "business_name",
            "addresses",
            "created_at",
            "updated_at",
        ]

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
        addresses = validated_data.pop("addresses")
        user = User.objects.create_user(**user_data)
        business_partner = BusinessPartner.objects.create(user=user, **validated_data)
        business_partner_group, _ = Group.objects.get_or_create(name="BusinessPartner")
        user.groups.add(business_partner_group)
        for address in addresses:
            address_obj, _ = Address.objects.get_or_create(**address)
            business_partner.addresses.add(address_obj)
        return business_partner


class DeliveryPartnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = DeliveryPartner
        fields = ["id", "user", "company_name", "addresses", "created_at", "updated_at"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        delivery_partner = DeliveryPartner.objects.create(user=user, **validated_data)
        return delivery_partner


class DevliveryRequestSerializer(serializers.ModelSerializer):
    requester = BusinessPartnerSerializer(read_only=True)

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

    def create(self, validated_data):
        validated_data["requester"] = self.context["request"].user.partner_profile
        return super().create(validated_data)
