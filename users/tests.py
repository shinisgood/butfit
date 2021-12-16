import json


from .models import User, Reservation, Credit
from django.test import TestCase
from django.test import Client
from unittest.mock import patch, MagicMock


class UserTest(TestCase):
    def setUp(self):
        # 관리자
        User.objects.create(
            email="admin@admin.com",
            phone_number="01012340000",
            is_staff=True,
            is_superuser=True,
        )
        User.objects.create(
            email="test@test.com",
            phone_number="01012340001",
        )

    def tearDown(self):
        Credit.objects.all().delete()
        User.objects.all().delete()

    def test_user_credit_over_100000_post_success(self):
        client = Client()
        User.objects.get(email="test@test.com")
        credit = {"user": 1, "credit": 100000}
        response = client.post(
            "/users/credits/", json.dumps(credit), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
