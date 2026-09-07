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
    status = models.CharField(max_length=30, default="submitted")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title