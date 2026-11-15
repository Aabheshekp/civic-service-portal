from django.contrib import admin
from django.urls import path, include
from portal import views

urlpatterns = [path("admin/", admin.site.urls), path("accounts/", include("django.contrib.auth.urls")), path("", views.home, name="home"), path("requests/new/", views.new_request, name="new_request"), path("requests/<int:pk>/", views.case_detail, name="case_detail"), path("requests/<int:pk>/status/", views.update_status, name="update_status"), path("staff/", views.staff_queue, name="staff_queue"), path("staff/export.csv", views.export_cases, name="export_cases")]
