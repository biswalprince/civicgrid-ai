from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    """Return the service health status for uptime checks."""
    return Response({"status": "ok", "service": "civicgrid-backend"})
