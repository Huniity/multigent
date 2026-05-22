FROM python:3.14.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY srcs/backend/requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY srcs/backend .

RUN mkdir -p /app/logs && chmod 777 /app/logs

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]