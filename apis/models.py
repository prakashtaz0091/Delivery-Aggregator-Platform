from django.db import models
from django.contrib.auth.models import User


class BusinessPartner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


DELIVERY_STATUS = (
    ("PENDING", "PENDING"),
    ("DECLINED", "DECLINED"),
    ("PICKED_UP", "PICKED_UP"),
    ("DISPATCHED", "DISPATCHED"),
    ("IN_TRANSIT", "IN_TRANSIT"),
    ("DELIVERED", "DELIVERED"),
)


class DeliveryRequest(models.Model):
    description = models.CharField(max_length=100)
    status = models.CharField(
        max_length=100, choices=DELIVERY_STATUS, default="PENDING"
    )

    requester = models.ForeignKey(
        BusinessPartner, on_delete=models.DO_NOTHING, related_name="requester"
    )
    receiver_address = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
