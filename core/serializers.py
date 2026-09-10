from rest_framework import serializers

from .models import CitizenRequest


class CitizenRequestSerializer(serializers.ModelSerializer):
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