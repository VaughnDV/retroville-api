FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN apt-get update && apt-get install -y cron && apt-get install -y nano
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python ./cron.py

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000

# Migrates the database, uploads staticfiles, and runs the production server
CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - retroville.wsgi:application
