FROM deanayalon/poetry AS deps

# Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install

FROM python:3.12-slim-bookworm
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=docker /usr/local/bin/docker /usr/local/bin/docker
RUN mkdir exports
COPY --from=deps /app/.venv ./.venv

COPY main.py .

ENTRYPOINT ["python3", "main.py"]