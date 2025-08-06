from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from apis.models import BusinessPartner, DeliveryPartner, DeliveryRequest
from django.test import TestCase


class BusinessPartnerRegisterTests(APITestCase):
    def setUp(self):
        self.url = reverse("register-business-partner")
        self.payload = {
            "user": {
                "username": "prakash123",
                "email": "prakash@example.com",
                "password": "securepassword123",
            },
            "business_name": "Tajpuriya Traders",
            "address": "Kathmandu, Nepal",
        }

    def test_create_business_partner_success(self):
        response = self.client.post(self.url, data=self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["business_name"], "Tajpuriya Traders")
        self.assertTrue(User.objects.filter(username="prakash123").exists())
        self.assertTrue(
            BusinessPartner.objects.filter(business_name="Tajpuriya Traders").exists()
        )

    def test_missing_required_fields(self):
        invalid_payload = {
            "user": {
                "username": "prakash123",
                "email": "prakash@example.com",
                # missing password
            },
            "business_name": "",
            "address": "",
        }

        response = self.client.post(self.url, data=invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ModelsTestCase(TestCase):
    def setUp(self):
        # Create users
        self.business_user = User.objects.create_user(
            username="bizuser", email="biz@example.com", password="testpass"
        )
        self.delivery_user = User.objects.create_user(
            username="deluser", email="del@example.com", password="testpass"
        )

        # Create BusinessPartner
        self.business_partner = BusinessPartner.objects.create(
            user=self.business_user,
            business_name="Tajpuriya Traders",
            address="Kathmandu, Nepal",
        )

        # Create DeliveryPartner
        self.delivery_partner = DeliveryPartner.objects.create(
            user=self.delivery_user, company_name="FastDelivery Pvt. Ltd."
        )

    def test_business_partner_creation(self):
        self.assertEqual(self.business_partner.business_name, "Tajpuriya Traders")
        self.assertEqual(str(self.business_partner), "Tajpuriya Traders")
        self.assertEqual(self.business_partner.user.username, "bizuser")

    def test_delivery_partner_creation(self):
        self.assertEqual(self.delivery_partner.company_name, "FastDelivery Pvt. Ltd.")
        self.assertEqual(str(self.delivery_partner), "FastDelivery Pvt. Ltd.")
        self.assertEqual(self.delivery_partner.user.email, "del@example.com")

    def test_delivery_request_creation(self):
        delivery_request = DeliveryRequest.objects.create(
            description="Send documents to Lalitpur",
            requester=self.business_partner,
            receiver_name="Manish Thapa",
            receiver_address="Lalitpur, Nepal",
            status="PENDING",
        )

        self.assertEqual(str(delivery_request), "Send documents to Lalitpur")
        self.assertEqual(delivery_request.status, "PENDING")
        self.assertEqual(delivery_request.requester.business_name, "Tajpuriya Traders")
        self.assertEqual(delivery_request.receiver_name, "Manish Thapa")
