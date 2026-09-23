from core.models import CitizenRequest, DistrictProfile, InfrastructureIndicator
from types import SimpleNamespace
from unittest.mock import patch

import httpx
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import DistrictProfile, InfrastructureIndicator
from core.services.infrastructure_service import calculate_infrastructure_gap
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

class InfrastructureGapTests(APITestCase):
    def setUp(self):
        self.district = DistrictProfile.objects.create(
            district_name="Test District",
            state="Odisha",
            population=100000,
        )

    def test_coverage_is_converted_to_gap_score(self):
        InfrastructureIndicator.objects.create(
            district=self.district,
            category="water",
            indicator="coverage",
            value=82,
            unit="percent",
        )

        gap = calculate_infrastructure_gap(
            district=self.district,
            category="water",
        )

        self.assertEqual(gap, 2)

    def test_zero_coverage_returns_maximum_gap(self):
        InfrastructureIndicator.objects.create(
            district=self.district,
            category="water",
            indicator="coverage",
            value=0,
            unit="percent",
        )

        gap = calculate_infrastructure_gap(
            district=self.district,
            category="water",
        )

        self.assertEqual(gap, 10)

    def test_missing_indicator_returns_none(self):
        gap = calculate_infrastructure_gap(
            district=self.district,
            category="water",
        )

        self.assertIsNone(gap)

    def test_non_percentage_indicator_returns_none(self):
        InfrastructureIndicator.objects.create(
            district=self.district,
            category="water",
            indicator="coverage",
            value=82,
            unit="liters",
        )

        gap = calculate_infrastructure_gap(
            district=self.district,
            category="water",
        )

        self.assertIsNone(gap)


class CitizenRequestIntegrationTests(APITestCase):
    def setUp(self):
        self.district = DistrictProfile.objects.create(
            district_name="Khordha",
            state="Odisha",
            population=100000,
            households=25000,
            urban_population=60000,
            rural_population=40000,
            literacy_rate=75,
            sc_population=10000,
            st_population=5000,
        )

        InfrastructureIndicator.objects.create(
            district=self.district,
            category="water",
            indicator="coverage",
            value=82,
            unit="percent",
            source="Test infrastructure dataset",
            data_year=2011,
        )

    @patch("core.views.extract_request_details")
    def test_request_creation_uses_infrastructure_gap(
        self,
        mock_extract,
    ):
        mock_extract.return_value = {
            "summary": "Severe drinking water shortage in Khordha.",
            "category": "water",
            "location": "Khordha district",
            "language": "English",
            "severity": 8,
            "affected_population": 7,
            "infrastructure_gap": 9,
            "vulnerability": 7,
        }

        response = self.client.post(
            "/api/requests/",
            {
                "description": (
                    "There is a severe shortage of drinking water "
                    "in Khordha district."
                )
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        citizen_request = CitizenRequest.objects.get(
            id=response.json()["id"]
        )

        self.assertEqual(
            citizen_request.district,
            self.district,
        )

        # 82% coverage should override Gemini's gap of 9
        self.assertEqual(
            citizen_request.infrastructure_gap,
            2,
        )

        # 8×4 + 7×3 + 2×2 + 7 = 64
        # 64 × 1.05 = 67.2 → 67
        self.assertEqual(
            citizen_request.priority_score,
            62,
        )

    @patch("core.views.extract_request_details")
    def test_unknown_location_falls_back_to_gemini_gap(
        self,
        mock_extract,
    ):
        mock_extract.return_value = {
            "summary": "Severe water shortage in an unknown location.",
            "category": "water",
            "location": "Unknown Village",
            "language": "English",
            "severity": 8,
            "affected_population": 7,
            "infrastructure_gap": 9,
            "vulnerability": 7,
        }

        response = self.client.post(
            "/api/requests/",
            {
                "description": "There is a severe water shortage."
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        citizen_request = CitizenRequest.objects.get(
            id=response.json()["id"]
        )

        self.assertIsNone(citizen_request.district)

        # No infrastructure indicator is available,
        # so Gemini's value is preserved.
        self.assertEqual(
            citizen_request.infrastructure_gap,
            9,
        )

    @patch("core.views.generate_project_recommendation")
    def test_recommendation_returns_infrastructure_evidence(
        self,
        mock_recommendation,
    ):
        mock_recommendation.return_value = {
            "recommended_project": "Rural Water Supply Expansion",
            "target_area": "Khordha district",
            "reason": "Water infrastructure requires improvement.",
            "expected_impact": "HIGH",
            "implementation_priority": "HIGH",
        }

        citizen_request = CitizenRequest.objects.create(
            title="Water shortage",
            description="Severe water shortage in Khordha.",
            category="water",
            location="Khordha district",
            language="English",
            severity=8,
            affected_population=7,
            infrastructure_gap=2,
            vulnerability=7,
            summary="Severe water shortage in Khordha.",
            status="submitted",
            priority_score=67,
            district=self.district,
        )

        response = self.client.post(
            f"/api/requests/{citizen_request.id}/recommend/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = response.json()

        self.assertIn("evidence", data)
        self.assertIn("infrastructure", data["evidence"])

        infrastructure = data["evidence"]["infrastructure"]

        self.assertEqual(len(infrastructure), 1)

        self.assertEqual(
            infrastructure[0]["category"],
            "water",
        )

        self.assertEqual(
            infrastructure[0]["value"],
            82.0,
        )

        self.assertEqual(
            infrastructure[0]["source"],
            "Test infrastructure dataset",
        )

        self.assertEqual(
            infrastructure[0]["data_year"],
            2011,
        )


class DashboardSummaryTests(APITestCase):
    def setUp(self):
        self.district = DistrictProfile.objects.create(
            district_name="Khordha",
            state="Odisha",
            population=100000,
            households=25000,
            urban_population=60000,
            rural_population=40000,
            literacy_rate=75,
            sc_population=10000,
            st_population=5000,
        )

        InfrastructureIndicator.objects.create(
            district=self.district,
            category="water",
            indicator="coverage",
            value=82,
            unit="percent",
            source="Test infrastructure dataset",
            data_year=2011,
        )

        CitizenRequest.objects.create(
            title="Water shortage",
            description="Water shortage",
            category="water",
            location="Khordha",
            language="English",
            severity=8,
            affected_population=7,
            infrastructure_gap=2,
            vulnerability=7,
            summary="Water shortage",
            status="submitted",
            priority_score=70,
            district=self.district,
        )

        CitizenRequest.objects.create(
            title="Bhubaneswar water shortage",
            description="Water shortage in Bhubaneswar",
            category="water",
            location="Bhubaneswar",
            language="English",
            severity=7,
            affected_population=6,
            infrastructure_gap=2,
            vulnerability=6,
            summary="Water shortage in Bhubaneswar",
            status="submitted",
            priority_score=65,
            district=self.district,
        )

        CitizenRequest.objects.create(
            title="Road damage",
            description="Damaged road",
            category="roads",
            location="Cuttack",
            language="English",
            severity=5,
            affected_population=4,
            infrastructure_gap=3,
            vulnerability=2,
            summary="Damaged road",
            status="submitted",
            priority_score=45,
        )

        CitizenRequest.objects.create(
            title="Minor issue",
            description="Minor infrastructure issue",
            category="other",
            location="Puri",
            language="English",
            severity=2,
            affected_population=1,
            infrastructure_gap=1,
            vulnerability=1,
            summary="Minor issue",
            status="submitted",
            priority_score=20,
        )

    def test_dashboard_summary_returns_expected_aggregates(self):
        response = self.client.get("/api/dashboard/summary/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["total_requests"], 4)
        self.assertEqual(data["high_priority"], 2)
        self.assertEqual(data["demand_hotspots"], 1)
        self.assertEqual(data["infrastructure_indicators"], 1)

        self.assertEqual(
            data["priority_distribution"],
            {
                "HIGH": 2,
                "MEDIUM": 1,
                "LOW": 1,
            },
        )

        locations = {
            item["location"]: item["count"]
            for item in data["demand_by_location"]
        }

        self.assertEqual(locations["Khordha"], 2)
        self.assertEqual(locations["Cuttack"], 1)
        self.assertEqual(locations["Puri"], 1)