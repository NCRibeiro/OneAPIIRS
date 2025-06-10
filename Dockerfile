# ────────────────────────────────────────────────
# Stage 1 — Builder
# ────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /install

# Copia arquivos de dependências primeiro (melhora o cache do Docker)
COPY requirements.txt .
COPY requirements-dev.txt .

# Atualiza pip e instala dependências
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    libyaml-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt -r requirements-dev.txt

# ────────────────────────────────────────────────
# Stage 2 — Runtime Final
# ────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libyaml-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia dependências Python instaladas
COPY --from=builder /install /usr/local

# Copia o código da aplicação
COPY . .

EXPOSE 8000

# Comando para executar a aplicação
# CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
