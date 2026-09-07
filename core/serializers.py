from rest_framework import serializers

from .models import CitizenRequest


class CitizenRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenRequest
        fields = "__all__"

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Title cannot be empty."
            )
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Description cannot be empty."
            )
        return value

    def validate_location(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Location cannot be empty."
            )
        return value