from django.db.models import Avg, Sum, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status, viewsets
from .services.gemini_service import (
    GeminiServiceError,
    extract_request_details,
)
from .services.location_service import (
    normalize_location,
    get_district_for_location,
)
from .models import CitizenRequest, DistrictProfile
from .serializers import CitizenRequestSerializer


@api_view(["GET"])
def health_check(request):
    """Return the service health status for uptime checks."""

    return Response({
        "status": "ok",
        "service": "civicgrid-backend",
    })


@api_view(["POST"])
def calculate_priority(request, request_id):
    """Calculate and save a priority score for a citizen request."""

    try:
        citizen_request = CitizenRequest.objects.get(id=request_id)
    except CitizenRequest.DoesNotExist:
        return Response(
            {"error": "Citizen request not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    required_fields = [
        "severity",
        "affected_population",
        "infrastructure_gap",
        "vulnerability",
    ]

    scores = {}

    for field in required_fields:
        value = request.data.get(field)

        if isinstance(value, bool) or not isinstance(value, int):
            return Response(
                {
                    "error": f"{field} must be an integer between 0 and 10."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if value < 0 or value > 10:
            return Response(
                {
                    "error": f"{field} must be an integer between 0 and 10."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        scores[field] = value

    priority_score = (
        scores["severity"] * 4
        + scores["affected_population"] * 3
        + scores["infrastructure_gap"] * 2
        + scores["vulnerability"]
    )

    if priority_score < 30:
        recommendation = "Low priority infrastructure request"
    elif priority_score < 60:
        recommendation = "Medium priority infrastructure request"
    else:
        recommendation = "High priority infrastructure request"

    citizen_request.priority_score = priority_score
    citizen_request.save(update_fields=["priority_score"])

    return Response({
        "request_id": citizen_request.id,
        "priority_score": priority_score,
        "recommendation": recommendation,
    })

@api_view(["GET"])
def demand_hotspots(request):
    """Return infrastructure demand aggregated by location."""

    hotspots = (
        CitizenRequest.objects
        .values("location")
        .annotate(
            request_count=Count("id"),
            average_priority_score=Avg("priority_score"),
            average_severity=Avg("severity"),
            total_affected_population=Sum("affected_population"),
        )
        .order_by("-average_priority_score")
    )

    results = []

    for hotspot in hotspots:
        average_priority = hotspot["average_priority_score"] or 0

        if average_priority < 30:
            demand_level = "LOW"
        elif average_priority < 60:
            demand_level = "MEDIUM"
        else:
            demand_level = "HIGH"

        results.append({
            "location": hotspot["location"],
            "request_count": hotspot["request_count"],
            "average_priority_score": round(average_priority, 2),
            "average_severity": round(hotspot["average_severity"] or 0, 2),
            "total_affected_population": (
                hotspot["total_affected_population"] or 0
            ),
            "demand_level": demand_level,
        })

    return Response(results)


class CitizenRequestViewSet(viewsets.ModelViewSet):
    serializer_class = CitizenRequestSerializer

    def get_queryset(self):
        queryset = CitizenRequest.objects.all().order_by("-created_at")

        category = self.request.query_params.get("category")
        location = self.request.query_params.get("location")
        status_filter = self.request.query_params.get("status")

        if category:
            queryset = queryset.filter(category__iexact=category)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if status_filter:
            queryset = queryset.filter(status__iexact=status_filter)


        return queryset

    def perform_create(self, serializer):
        description = serializer.validated_data["description"]

        try:
            details = extract_request_details(description)
        except GeminiServiceError as exc:
            raise serializers.ValidationError({
                "gemini": str(exc)
            })

        priority_score = (
            details["severity"] * 4
            + details["affected_population"] * 3
            + details["infrastructure_gap"] * 2
            + details["vulnerability"]
        )

        title = details["summary"][:200]

        normalized_location = normalize_location(details["location"])

        district_name = get_district_for_location(normalized_location)

        district = None

        if district_name:
            district = DistrictProfile.objects.filter(
                district_name=district_name
            ).first()

        serializer.save(
            title=title,
            category=details["category"],
            location=normalized_location,
            district=district,
            language=details["language"],
            severity=details["severity"],
            affected_population=details["affected_population"],
            infrastructure_gap=details["infrastructure_gap"],
            vulnerability=details["vulnerability"],
            summary=details["summary"],
            priority_score=priority_score,
            status="submitted",
        )
