# Civic Service Portal

A secure-by-default Django case management portal for local service requests. Residents can submit and follow cases; staff can triage queues, assign categories, update status, and leave an auditable timeline. It ships with Django authentication, CSRF-protected forms, SQLite for local use, an admin console, and container deployment.

## Start locally
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate --run-syncdb
python manage.py createsuperuser
python manage.py runserver
```
Visit `http://127.0.0.1:8000`. Sign in at `/accounts/login/`; staff users can manage the queue at `/staff/` and Django admin at `/admin/`.

## Features
- Authenticated case intake with category, location, and detailed description.
- Resident-scoped case list and staff-wide queue with status filters.
- Staff-only transitions and assignment; every status update creates a timeline event.
- CSRF protection, safe HTML templates, server-side validation, and Django's password handling.
- CSV queue export for staff, audit view, and operational dashboard.

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, and `DJANGO_ALLOWED_HOSTS` in deployment. Use a production database and HTTPS before serving public traffic. See [operations](docs/operations.md). MIT license.
