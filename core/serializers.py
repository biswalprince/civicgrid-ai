from rest_framework import serializers

from .models import CitizenRequest


class CitizenRequestSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(
        source="district.district_name",
        read_only=True,
    )
    priority_breakdown = serializers.SerializerMethodField()

    def get_priority_breakdown(self, obj):
        from .services.priority_service import get_priority_breakdown

        details = {
            "severity": obj.severity,
            "affected_population": obj.affected_population,
            "infrastructure_gap": obj.infrastructure_gap,
            "vulnerability": obj.vulnerability,
        }

        return get_priority_breakdown(
            details=details,
            district=obj.district,
        )
    
    class Meta:
        model = CitizenRequest
        fields = "__all__"
        read_only_fields = [
            "title",
            "category",
            "location",
            "language",
            "severity",
            "affected_population",
            "infrastructure_gap",
            "vulnerability",
            "summary",
            "priority_score",
            "status",
            "created_at",
        ]

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Description cannot be empty."
            )
        return value