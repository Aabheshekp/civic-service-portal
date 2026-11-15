from django.conf import settings
from django.db import models

class ServiceCase(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        TRIAGED = "triaged", "Triaged"
        IN_PROGRESS = "in_progress", "In progress"
        WAITING = "waiting", "Waiting on resident"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    class Category(models.TextChoices):
        ROADS = "roads", "Roads and sidewalks"
        WASTE = "waste", "Waste and recycling"
        PARKS = "parks", "Parks and public spaces"
        LIGHTING = "lighting", "Street lighting"
        OTHER = "other", "Other"

    reference = models.CharField(max_length=16, unique=True, editable=False)
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="service_cases")
    category = models.CharField(max_length=24, choices=Category.choices)
    location = models.CharField(max_length=180)
    summary = models.CharField(max_length=140)
    description = models.TextField(max_length=5000)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.RECEIVED)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_cases")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.reference:
            super().save(*args, **kwargs)
            self.reference = f"CSR-{self.created_at:%y%m}-{self.pk:05d}"
            return super().save(update_fields=["reference"])
        return super().save(*args, **kwargs)

    def __str__(self): return f"{self.reference} · {self.summary}"

class CaseEvent(models.Model):
    case = models.ForeignKey(ServiceCase, on_delete=models.CASCADE, related_name="events")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    from_status = models.CharField(max_length=24, choices=ServiceCase.Status.choices, blank=True)
    to_status = models.CharField(max_length=24, choices=ServiceCase.Status.choices)
    note = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
