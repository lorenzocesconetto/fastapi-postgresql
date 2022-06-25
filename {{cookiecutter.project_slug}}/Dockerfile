FROM python:3.10.4-slim-bullseye AS base

WORKDIR /application

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Needed to build/compile psycopg2 (and other Python extensions written in C or C++)
RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y build-essential
RUN apt-get install -y libpq-dev

# Copy packaging requirements
COPY ./pyproject.toml ./poetry.lock ./

ENTRYPOINT ["bash", "./boot.sh"]

###################
# Development
###################
FROM base AS development

# Install dev dependencies as well
RUN poetry install --no-root

COPY . .

CMD "development"

###################
# Celery worker
###################
FROM base AS celery_worker

# Install production dependencies
RUN poetry install --no-root --no-dev

COPY . .

RUN chmod +x scripts/worker-start.sh

ENTRYPOINT ["bash", "./scripts/worker-start.sh"]

###################
# Production
###################
FROM base AS production

# Install production dependencies
RUN poetry install --no-root --no-dev

COPY . .

CMD "production"
