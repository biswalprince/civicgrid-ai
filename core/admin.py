from django.contrib import admin
from .models import CitizenRequest
from .models import InfrastructureIndicator

admin.site.register(CitizenRequest)
admin.site.register(InfrastructureIndicator)