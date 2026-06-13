FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# This runs migrations, creates your admin account, and starts the server
CMD ["sh", "-c", "python manage.py migrate && DJANGO_SUPERUSER_PASSWORD=admin1234 python manage.py createsuperuser --username admin --email admin@uddoktardokan.com --noinput || true && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4"]
