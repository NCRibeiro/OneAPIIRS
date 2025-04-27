# Etapa de construção
FROM python:3.13-alpine AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    build-base gcc libffi-dev musl-dev \
    python3-dev libpq libpq-dev openssl-dev \
    && rm -rf /var/cache/apk/*

COPY requirements.txt .

# Instala pacotes na pasta /install
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# ──────────────────────────────────────────────
# Etapa de runtime
# ──────────────────────────────────────────────
FROM python:3.13-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 8000
EXPOSE 8050

ARG ENTRY=api
ENV ENTRYPOINT_MODE=${ENTRY}

CMD ["sh", "-c", "\
    if [ ! -f app/main.py ]; then \
        echo '[ERRO] Arquivo app/main.py não encontrado! Verifique a estrutura do projeto.' && exit 1; \
    fi; \
    if [ \"$ENTRYPOINT_MODE\" = \"dash\" ]; then \
        if [ ! -f app/dashboard/dashboard.py ]; then \
            echo '[ERRO] Arquivo app/dashboard/dashboard.py não encontrado! Verifique a estrutura do projeto.' && exit 1; \
        fi; \
        echo '[INFO] Iniciando Dashboard...'; \
        python app/dashboard/dashboard.py; \
    else \
        echo '[INFO] Iniciando API FastAPI...'; \
        uvicorn app.main:app --host 0.0.0.0 --port 8000\
    fi"]
