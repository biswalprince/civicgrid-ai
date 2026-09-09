from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import CitizenRequest
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