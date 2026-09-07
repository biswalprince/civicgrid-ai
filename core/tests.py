from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class HealthCheckTests(APITestCase):
    def test_health_check_returns_expected_response(self):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"status": "ok", "service": "civicgrid-backend"},
        )
