from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class DeliveryPartner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    addresses = models.ManyToManyField(Address, related_name="delivery_partners")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class BusinessPartner(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="partner_profile"
    )
    business_name = models.CharField(max_length=200)
    addresses = models.ManyToManyField(Address, related_name="businesses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


class DeliveryRequest(models.Model):
    description = models.CharField(max_length=100)

    DELIVERY_STATUS = (
        ("PENDING", "PENDING"),
        ("DECLINED", "DECLINED"),
        ("PICKED_UP", "PICKED_UP"),
        ("DISPATCHED", "DISPATCHED"),
        ("IN_TRANSIT", "IN_TRANSIT"),
        ("DELIVERED", "DELIVERED"),
    )

    status = models.CharField(
        max_length=100, choices=DELIVERY_STATUS, default="PENDING"
    )
    pending_sync = models.BooleanField(default=True)

    requester = models.ForeignKey(
        BusinessPartner, on_delete=models.DO_NOTHING, related_name="requester"
    )
    receiver_address = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)

    delivery_partner = models.ForeignKey(
        DeliveryPartner,
        on_delete=models.DO_NOTHING,
        related_name="delivery_partners",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
