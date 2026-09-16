from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CitizenRequestViewSet,
    InfrastructureIndicatorViewSet,
    calculate_priority,
    demand_hotspots,
    generate_recommendation,
    health_check,
)

router = DefaultRouter()

router.register(
    "requests",
    CitizenRequestViewSet,
    basename="citizen-request",
)

router.register(
    "infrastructure-indicators",
    InfrastructureIndicatorViewSet,
    basename="infrastructure-indicator",
)

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path(
        "requests/<int:request_id>/calculate-priority/",
        calculate_priority,
        name="calculate-priority",
    ),
    path(
        "requests/<int:request_id>/recommend/",
        generate_recommendation,
        name="generate-recommendation",
    ),
    path("hotspots/", demand_hotspots, name="demand-hotspots"),
    path("", include(router.urls)),
]