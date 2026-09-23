from django.db.models import Avg, Sum, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status, viewsets
from .services.gemini_service import (
    GeminiServiceError,
    extract_request_details,
    generate_project_recommendation,
)
from .services.location_service import (
    normalize_location,
    get_district_for_location,
)
from .models import (
    CitizenRequest, 
    DistrictProfile,
    InfrastructureIndicator,
)
from .serializers import (
    CitizenRequestSerializer,
    InfrastructureIndicatorSerializer,
)
from .services.infrastructure_service import(
    calculate_infrastructure_gap,
)
from .services.priority_service import (
    calculate_priority_score,
    get_priority_breakdown,
)


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

@api_view(["GET"])
def dashboard_summary(request):
    """Return aggregated data for the policymaker dashboard."""

    total_requests = CitizenRequest.objects.count()

    high_priority = CitizenRequest.objects.filter(
        priority_score__gte=60
    ).count()

    infrastructure_indicators = InfrastructureIndicator.objects.count()

    priority_distribution = {
        "HIGH": CitizenRequest.objects.filter(
            priority_score__gte=60
        ).count(),
        "MEDIUM": CitizenRequest.objects.filter(
            priority_score__gte=30,
            priority_score__lt=60,
        ).count(),
        "LOW": CitizenRequest.objects.filter(
            priority_score__lt=30
        ).count(),
    }

    location_data = (
        CitizenRequest.objects
        .values("location")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    demand_by_location = [
        {
            "location": item["location"],
            "count": item["count"],
        }
        for item in location_data
    ]

    demand_hotspot_count = sum(
        1 for item in demand_by_location
        if item["count"] >= 2
    )

    return Response({
        "total_requests": total_requests,
        "high_priority": high_priority,
        "demand_hotspots": demand_hotspot_count,
        "infrastructure_indicators": infrastructure_indicators,
        "priority_distribution": priority_distribution,
        "demand_by_location": demand_by_location,
    })

@api_view(["POST"])
def generate_recommendation(request, request_id):
    """Generate an AI infrastructure project recommendation."""

    try:
        citizen_request = CitizenRequest.objects.get(id=request_id)
    except CitizenRequest.DoesNotExist:
        return Response(
            {"error": "Citizen request not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    request_details = {
        "category": citizen_request.category,
        "location": citizen_request.location,
        "language": citizen_request.language,
        "severity": citizen_request.severity,
        "affected_population": citizen_request.affected_population,
        "infrastructure_gap": citizen_request.infrastructure_gap,
        "vulnerability": citizen_request.vulnerability,
        "summary": citizen_request.summary,
    }

    priority_breakdown = {
    "severity": citizen_request.severity * 4,
    "affected_population": citizen_request.affected_population * 3,
    "infrastructure_gap": citizen_request.infrastructure_gap * 2,
    "vulnerability": citizen_request.vulnerability,
    "base_score": (
        citizen_request.severity * 4
        + citizen_request.affected_population * 3
        + citizen_request.infrastructure_gap * 2
        + citizen_request.vulnerability
    ),
    "final_score": citizen_request.priority_score,
}

    district_context = None

    if citizen_request.district:
        district = citizen_request.district

        district_context = {
            "district_name": district.district_name,
            "state": district.state,
            "population": district.population,
            "households": district.households,
            "urban_population": district.urban_population,
            "rural_population": district.rural_population,
            "literacy_rate": district.literacy_rate,
            "sc_population": district.sc_population,
            "st_population": district.st_population,
        }

    infrastructure_context = []

    if citizen_request.district:
        indicators = InfrastructureIndicator.objects.filter(
            district=citizen_request.district
        ).order_by("category", "indicator")

        infrastructure_context = [
            {
                "category": indicator.category,
                "indicator": indicator.indicator,
                "value": indicator.value,
                "unit": indicator.unit,
                "source": indicator.source,
                "data_year": indicator.data_year,
            }
            for indicator in indicators
        ]

    try:
        recommendation = generate_project_recommendation(
            request_details=request_details,
            priority_breakdown=priority_breakdown,
            district_context=district_context,
            infrastructure_context=infrastructure_context,
        )
    except GeminiServiceError as exc:
        return Response(
            {"error": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response({
        "request_id": citizen_request.id,
        "priority_score": citizen_request.priority_score,
        "recommendation": recommendation,
        "evidence": {
        "infrastructure": infrastructure_context,
        },
    })


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

        title = details["summary"][:200]

        normalized_location = normalize_location(details["location"])

        district_name = get_district_for_location(normalized_location)

        district = None

        if district_name:
            district = DistrictProfile.objects.filter(
                district_name=district_name
            ).first()

        infrastructure_gap = calculate_infrastructure_gap(
            district=district,
            category=details["category"],
        )
        if infrastructure_gap is not None:
            details["infrastructure_gap"] = infrastructure_gap
            
        priority_score = calculate_priority_score(
                    details=details,
                    district=district,
                )

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

class InfrastructureIndicatorViewSet(viewsets.ModelViewSet):
    queryset = InfrastructureIndicator.objects.select_related(
        "district"
    ).all().order_by("district__district_name", "category", "indicator")

    serializer_class = InfrastructureIndicatorSerializer

    def get_queryset(self):
        queryset = self.queryset

        category = self.request.query_params.get("category")
        district = self.request.query_params.get("district")

        if category:
            queryset = queryset.filter(category__iexact=category)

        if district:
            queryset = queryset.filter(
                district__district_name__icontains=district
            )

        return queryset