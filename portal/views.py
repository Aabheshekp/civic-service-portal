import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import CaseForm, StatusForm
from .models import CaseEvent, ServiceCase

def home(request):
    cases = ServiceCase.objects.select_related("resident", "assigned_to")
    if request.user.is_authenticated and not request.user.is_staff: cases = cases.filter(resident=request.user)
    elif not request.user.is_authenticated: cases = cases.none()
    counts = {status: cases.filter(status=status).count() for status, _ in ServiceCase.Status.choices}
    return render(request, "portal/home.html", {"cases": cases[:50], "counts": counts})

@login_required
def new_request(request):
    form = CaseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        case = form.save(commit=False); case.resident = request.user; case.save()
        CaseEvent.objects.create(case=case, actor=request.user, to_status=case.status, note="Request submitted")
        messages.success(request, f"Request {case.reference} was submitted.")
        return redirect("case_detail", pk=case.pk)
    return render(request, "portal/case_form.html", {"form": form})

@login_required
def case_detail(request, pk):
    case = get_object_or_404(ServiceCase.objects.select_related("resident", "assigned_to").prefetch_related("events__actor"), pk=pk)
    if not request.user.is_staff and case.resident_id != request.user.id: raise Http404
    return render(request, "portal/case_detail.html", {"case": case, "status_form": StatusForm(initial={"status": case.status})})

@require_POST
@login_required
def update_status(request, pk):
    if not request.user.is_staff: raise Http404
    case = get_object_or_404(ServiceCase, pk=pk); form = StatusForm(request.POST)
    if form.is_valid():
        old = case.status; new = form.cleaned_data["status"]
        if new != old:
            case.status = new; case.save(update_fields=["status", "updated_at"])
            CaseEvent.objects.create(case=case, actor=request.user, from_status=old, to_status=new, note=form.cleaned_data["note"])
            messages.success(request, "Case status updated.")
        else: messages.info(request, "Status was unchanged.")
    else: messages.error(request, "Choose a valid status.")
    return redirect("case_detail", pk=case.pk)

@user_passes_test(lambda u: u.is_staff)
def staff_queue(request):
    cases = ServiceCase.objects.select_related("resident", "assigned_to")
    status = request.GET.get("status", "")
    if status in ServiceCase.Status.values: cases = cases.filter(status=status)
    return render(request, "portal/staff_queue.html", {"cases": cases[:500], "status": status, "statuses": ServiceCase.Status.choices})

@user_passes_test(lambda u: u.is_staff)
def export_cases(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="service-cases.csv"'
    writer = csv.writer(response); writer.writerow(["reference", "category", "summary", "location", "status", "resident", "created_at", "updated_at"])
    for c in ServiceCase.objects.select_related("resident").iterator(): writer.writerow([c.reference,c.category,c.summary,c.location,c.status,c.resident.username,c.created_at.isoformat(),c.updated_at.isoformat()])
    return response
