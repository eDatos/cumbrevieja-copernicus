FROM python:3.9.7-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PROJECT_DIR=/copernicus
WORKDIR $PROJECT_DIR

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

CMD ["python", "main.py", "-vn"]

