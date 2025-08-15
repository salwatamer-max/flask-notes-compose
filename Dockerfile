FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /code
USER appuser

ENV FLASK_APP=app.app:app \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=80

EXPOSE 80
CMD ["python", "-m", "flask", "run"]
