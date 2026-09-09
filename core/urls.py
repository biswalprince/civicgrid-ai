from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CitizenRequestViewSet,
    calculate_priority,
    health_check,
)


router = DefaultRouter()

router.register(
    "requests",
    CitizenRequestViewSet,
    basename="citizen-request",
)

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path(
        "requests/<int:request_id>/calculate-priority/",
        calculate_priority,
        name="calculate-priority",
    ),
    path("", include(router.urls)),
]