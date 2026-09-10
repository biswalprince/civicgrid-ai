from types import SimpleNamespace
from unittest.mock import patch

import httpx
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from core.services import gemini_service


class HealthCheckTests(APITestCase):
    def test_health_check_returns_expected_response(self):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"status": "ok", "service": "civicgrid-backend"},
        )


class GeminiServiceTests(APITestCase):
    @patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
    @patch("core.services.gemini_service.genai.Client")
    def test_extracts_structured_response(self, client_class):
        client = client_class.return_value
        client.models.generate_content.return_value = SimpleNamespace(
            text='''```json
            {"category":"water","location":"Ward 4","language":"en","severity":8,"affected_population":6,"infrastructure_gap":7,"vulnerability":5,"summary":"Water supply is interrupted."}
            ```'''
        )

        details = gemini_service.extract_request_details("There has been no water for days.")

        self.assertEqual(details["category"], "water")
        self.assertEqual(details["severity"], 8)
        kwargs = client.models.generate_content.call_args.kwargs
        self.assertEqual(kwargs["model"], gemini_service.GEMINI_MODEL)
        self.assertEqual(kwargs["config"].response_mime_type, "application/json")
        client.close.assert_called_once_with()

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_api_key_is_reported_without_exposure(self):
        with self.assertRaises(gemini_service.GeminiConfigurationError) as context:
            gemini_service.extract_request_details("A road is damaged.")

        self.assertEqual(str(context.exception), "Gemini is not configured. Set GEMINI_API_KEY.")

    @patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
    @patch("core.services.gemini_service.genai.Client")
    def test_network_error_is_wrapped_cleanly(self, client_class):
        client_class.return_value.models.generate_content.side_effect = httpx.ConnectError(
            "DNS lookup failed"
        )

        with self.assertRaises(gemini_service.GeminiRequestError) as context:
            gemini_service.extract_request_details("A road is damaged.")

        self.assertIn("DNS, network access, and proxy settings", str(context.exception))
        self.assertNotIn("test-key", str(context.exception))

    @patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
    @patch("core.services.gemini_service.genai.Client")
    def test_invalid_json_is_reported_cleanly(self, client_class):
        client_class.return_value.models.generate_content.return_value = SimpleNamespace(
            text="not json"
        )

        with self.assertRaises(gemini_service.GeminiResponseError):
            gemini_service.extract_request_details("A road is damaged.")

    @patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
    @patch("core.services.gemini_service.genai.Client")
    def test_missing_response_text_is_reported_cleanly(self, client_class):
        client_class.return_value.models.generate_content.return_value = SimpleNamespace(text=None)

        with self.assertRaises(gemini_service.GeminiResponseError):
            gemini_service.extract_request_details("A road is damaged.")
