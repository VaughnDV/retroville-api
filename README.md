# Retroville API

## Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

## Local Development

create a `.env` file in the root directory where `manage.py` lives, and populate the following:
```DJANGO_SETTINGS_MODULE=retroville.config 
DJANGO_CONFIGURATION=Local
DJANGO_SECRET_KEY=Local
ACCOUNT_SID=
API_KEY=
API_KEY_SECRET=
APP_SID=
PUSH_CREDENTIAL_SID=
REDIS_URL=redis://redis_db:6379
DEBUG=True
AUTHY_API_KEY=
NEWS_API_KEY=
```

Build for local development:
```bash
docker-compose build
```

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```


## Deployment

Make sure your changes are committed on Git...

Login to Heroku
```bash
heroku login
```

Login to Heroku containers
```bash
heroku container:login
```

Push changes to Heroku STAGE
```bash
heroku container:push web --remote stage
```

Release on Heroku STAGE
```bash
heroku container:release web --remote stage
```

RELEASED!!! :D

## Other 

Sometime you may need to work on the server:
```bash
heroku run bash --remote stage
```

Sometime you may need to see the logs on the server:
```bash
heroku logs -t --remote stage
```

Note that we have two environments, `stage` and `production`
