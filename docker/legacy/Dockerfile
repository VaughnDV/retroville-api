FROM python:3.6-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=retroville.config \
    DJANGO_CONFIGURATION=Local \
    DJANGO_SECRET_KEY=legacy-characterisation \
    DJANGO_DEBUG=yes

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && pip install --no-cache-dir 'pip<21' 'setuptools<50' \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apt-get purge -y gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . /code

CMD ["bash", "-c", "python wait_for_postgres.py && python manage.py test"]
