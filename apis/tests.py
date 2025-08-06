from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from apis.models import BusinessPartner


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
