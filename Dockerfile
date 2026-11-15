FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DJANGO_DEBUG=0 DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --run-syncdb && gunicorn civic_portal.wsgi:application --bind 0.0.0.0:8000"]
