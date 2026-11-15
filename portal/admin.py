from django.contrib import admin
from .models import CaseEvent, ServiceCase

class CaseEventInline(admin.TabularInline):
    model = CaseEvent; extra = 0; readonly_fields = ("actor", "from_status", "to_status", "note", "created_at")

@admin.register(ServiceCase)
class ServiceCaseAdmin(admin.ModelAdmin):
    list_display = ("reference", "summary", "category", "status", "resident", "assigned_to", "updated_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("reference", "summary", "location", "resident__username")
    readonly_fields = ("reference", "created_at", "updated_at")
    inlines = [CaseEventInline]

admin.site.register(CaseEvent)
