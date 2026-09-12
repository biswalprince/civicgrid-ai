from django.db import models


class CitizenRequest(models.Model):
    CATEGORY_CHOICES = [
        ("water", "Water Infrastructure"),
        ("roads", "Roads"),
        ("schools", "Schools"),
        ("sanitation", "Sanitation"),
        ("electricity", "Electricity"),
        ("healthcare", "Healthcare"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="water",
    )

    location = models.CharField(max_length=200)
    language = models.CharField(max_length=20, default="en")

    severity = models.IntegerField(default=0)
    affected_population = models.IntegerField(default=0)
    infrastructure_gap = models.IntegerField(default=0)
    vulnerability = models.IntegerField(default=0)

    summary = models.TextField(blank=True)

    status = models.CharField(max_length=30, default="submitted")
    priority_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    district = models.ForeignKey(
    "DistrictProfile",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="citizen_requests",
)

    def __str__(self):
        return self.title


class DistrictProfile(models.Model):
    district_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    population = models.IntegerField(default=0)
    households = models.IntegerField(default=0)

    urban_population = models.IntegerField(default=0)
    rural_population = models.IntegerField(default=0)

    literacy_rate = models.FloatField(default=0)
    sc_population = models.IntegerField(default=0)
    st_population = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.district_name}, {self.state}"