# Contributing

1. Keep resident cases private to their owner and authorized staff.
2. Preserve CSRF protection, template escaping, and audit events for status changes.
3. Document model changes and deployment settings; use migrations for production schema changes.
4. Never commit real resident or location data.
5. Use a focused branch and include a clear description of the user-visible change.

The CI workflow currently checks dependency installation and Python compilation.
