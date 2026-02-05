FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    postgresql-client \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir gunicorn

COPY . .

RUN mkdir -p backend/staticfiles backend/media \
  && chmod -R 755 backend/staticfiles backend/media

EXPOSE 8000

# IMPORTANT:
# - IN_DOCKER should be set by docker-compose (local), not baked into the image
# - On deploy, set DB_HOST/DB_PORT/etc via Container App env vars
CMD ["bash", "-lc", "cd backend && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn bcit_accreditation.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
