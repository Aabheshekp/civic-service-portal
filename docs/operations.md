# Operations and security

Use Django's built-in user and session framework. Requests require authentication; case details are scoped to the resident or staff. Staff queue, status changes, and CSV export are staff-only. Forms include CSRF tokens, templates escape user-controlled text, and the event table records status changes.

For deployment, provide a high-entropy `DJANGO_SECRET_KEY`, disable debug (`DJANGO_DEBUG=0`), set exact trusted hosts, terminate TLS, and use a persistent PostgreSQL database. Configure secure cookies and HTTPS proxy headers for the actual ingress. The development key and SQLite database are only for local demos. Do not store sensitive case details beyond an approved retention period.
