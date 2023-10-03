FROM python:3.12-slim as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

ENV POETRY_VERSION=1.4.0
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --only main


FROM python-base as production
ENV DEBIAN_FRONTEND noninteractive

COPY --from=builder-base $VENV_PATH $VENV_PATH

RUN \
  adduser nonroot \
  --uid 568 \
  --group \
  --system \
  --disabled-password \
  && \
  mkdir -p /app \
  && chown -R nonroot:nonroot /app \
  && chmod -R 775 /app \
  && chown -R nonroot:nonroot /opt/pysetup/.venv \
  && chmod -R 775 /opt/pysetup/.venv

USER nonroot

WORKDIR /app

COPY . .

# use the correct hostname in the docker-compose stack
RUN sed -i "s/localhost/azurite/" azurite.env

RUN ..$VENV_PATH/bin/activate

ENV PYTHONPATH="/app:$PYTHONPATH"

EXPOSE 8080
