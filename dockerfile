FROM python:3.12-slim-bookworm AS base
WORKDIR /app

FROM base AS deps

# Install poetry, create venv and add to path
RUN pip install pipx && pipx install poetry && pipx ensurepath && \
    python3 -m venv --without-pip .venv
ENV PATH="/app/.venv/bin:$PATH:/root/.local/bin"

# Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install

FROM base
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=docker /usr/local/bin/docker /usr/local/bin/docker

RUN mkdir exports
COPY --from=deps /app/.venv ./.venv

COPY main.py .

ENTRYPOINT ["python3", "main.py"]