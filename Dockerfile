# Etapa 1: Builder com Alpine + apk (correto)
FROM python:3.12-alpine AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependências básicas do sistema
RUN apk update && apk add --no-cache \
    build-base \
    gcc \
    libffi-dev \
    musl-dev \
    python3-dev \
    libpq \
    libpq-dev \
    openssl-dev \
    && rm -rf /var/cache/apk/*

COPY requirements.txt .

# Instala pacotes na pasta /install
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Etapa 2: Runtime mais leve
FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

