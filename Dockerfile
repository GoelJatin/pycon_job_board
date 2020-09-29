FROM python:3.8-slim-buster

COPY requirements.txt .

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    apt-utils \
    build-essential \
    libpq-dev; \
    apt-get clean; \
    apt update; \
    apt install -y curl git-all; \
    curl https://cli-assets.heroku.com/install.sh | sh; \
    apt remove; \
    apt-get purge; \
    pip install -r requirements.txt; \
    pip install --no-cache-dir pipenv; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

CMD [ "tail", "-f", "/dev/null" ]
