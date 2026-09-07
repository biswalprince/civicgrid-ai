from rest_framework import serializers
from .models import CitizenRequest


class CitizenRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenRequest
        fields = "__all__"