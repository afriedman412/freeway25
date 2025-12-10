# ---------- Stage 1: Builder ----------
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /venv /venv
COPY . .

EXPOSE 8000

ENV PATH="/venv/bin:$PATH"

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:live_app", "--bind", "0.0.0.0:8000"]
