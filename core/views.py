from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .models import CitizenRequest
from .serializers import CitizenRequestSerializer


@api_view(["GET"])
def health_check(request):
    """Return the service health status for uptime checks."""

    return Response({
        "status": "ok",
        "service": "civicgrid-backend",
    })


class CitizenRequestViewSet(viewsets.ModelViewSet):
    queryset = CitizenRequest.objects.all().order_by("-created_at")
    serializer_class = CitizenRequestSerializer