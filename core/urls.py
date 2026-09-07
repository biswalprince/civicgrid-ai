from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CitizenRequestViewSet, health_check


router = DefaultRouter()

router.register(
    "requests",
    CitizenRequestViewSet,
    basename="citizen-request",
)

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("", include(router.urls)),
]