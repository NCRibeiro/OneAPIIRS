# ────────────────────────────────────────────────────────
# Stage 1: Builder — instala dependências Python
# ────────────────────────────────────────────────────────
FROM python:3.13-alpine AS builder

WORKDIR /install

# 1) Instala dependências de sistema e atualiza pip
RUN apk add --no-cache \
      build-base libffi-dev musl-dev python3-dev postgresql-dev openssl-dev \
    && pip install --upgrade pip

# 2) Copia e instala as bibliotecas Python declaradas em requirements.txt
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ────────────────────────────────────────────────────────
# Stage 2: Runtime — imagem enxuta para rodar a aplicação
# ────────────────────────────────────────────────────────
FROM python:3.13-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Bibliotecas de runtime para Postgres
RUN apk add --no-cache postgresql-libs libpq

# Copia pacotes Python instalados no builder e o código da aplicação
COPY --from=builder /install /usr/local

COPY . .

# Exponha a porta da API
EXPOSE 8000
# Inicia o Uvicorn sem envolver shell, passando só os args que o uvicorn entende
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
