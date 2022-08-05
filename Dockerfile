FROM python:3.9-slim as python-base
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

ENV POETRY_VERSION=1.1.13
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev


FROM python-base as production
ENV FASTAPI_ENV=production
ENV DEBIAN_FRONTEND noninteractive

RUN \
  adduser nonroot \
  --uid 568 \
  --group \
  --system \
  --disabled-password \
  && \
  mkdir -p /app \
  && chown -R nonroot:nonroot /app \
  && chmod -R 775 /app

COPY --from=builder-base $VENV_PATH $VENV_PATH

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /app

USER nonroot

COPY . .

EXPOSE 8080

ENTRYPOINT /docker-entrypoint.sh $0 $@
