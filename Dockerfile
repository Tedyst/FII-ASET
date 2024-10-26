FROM python:3.12-slim AS base

ENV POETRY_HOME=/opt/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - && poetry --version

FROM base AS builder

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction

FROM base AS runner

WORKDIR /app
COPY --from=builder /app/.venv/ /app/.venv/

COPY . /app

EXPOSE 8000

RUN chmod +x /app/backend/entrypoint.sh

FROM runner AS development

WORKDIR /app/backend
ENTRYPOINT [ "/app/backend/entrypoint.sh" ]

FROM runner AS production

LABEL org.opencontainers.image.source=https://github.com/Tedyst/FII-ASET
LABEL org.opencontainers.image.description="FII-ASET Project"
LABEL org.opencontainers.image.licenses=MIT

ARG user=django
ARG group=django
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group} && \
    useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} && \
    chown -R ${uid}:${gid} /app

USER ${uid}:${gid}

WORKDIR /app/backend
ENTRYPOINT [ "/app/backend/entrypoint.sh" ]