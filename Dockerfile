# ---- Base Python image ----
FROM python:3.11-slim

# ---- Install MySQL dependencies ----
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ---- Set workdir ----
WORKDIR /app

# ---- Copy and install dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Set environment ----
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=backend.settings

# ---- Collect static files ----
RUN python manage.py collectstatic --noinput || true

# ---- Start the Gunicorn server ----
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
