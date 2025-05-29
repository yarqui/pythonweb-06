FROM python:3.12-slim AS base

# Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Poetry environment variables
ENV POETRY_VERSION=2.1.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_NO_INTERACTION=1

# Add Poetry to PATH
ENV PATH="${POETRY_HOME}/bin:${PATH}"

ENV APP_HOME=/app

# Application Setup
WORKDIR ${APP_HOME}

# Install
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}


# Copy only the dependency definition files first
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
RUN poetry install --no-interaction --no-root

# Copy the rest of the application
COPY ./src ./src
COPY ./migrations ./migrations/
COPY alembic.ini ./

# Runtime Configuration
VOLUME ["/app/storage/"]

EXPOSE 3000

CMD ["tail", "-f", "/dev/null"]