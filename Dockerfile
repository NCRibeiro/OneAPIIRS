# ────────────────────────────────────────────────
# Stage 1 — Builder
# ────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /install

# Instala dependências do sistema para build
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential gcc libffi-dev libpq-dev libssl-dev \
      libjpeg-dev zlib1g-dev libxml2-dev libxslt1-dev libyaml-dev \
      curl git \
 && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências (requirements e dev requirements)
COPY requirements*.txt ./

# Atualiza pip e instala pacotes Python no prefix /install
RUN pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/install \
      -r requirements.txt \
      -r requirements-dev.txt


# ────────────────────────────────────────────────
# Stage 2 — Runtime Final
# ────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Define variáveis Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependências de sistema para runtime
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libpq-dev libssl-dev libffi-dev \
      libjpeg-dev zlib1g-dev libxml2-dev libxslt1-dev libyaml-dev \
 && rm -rf /var/lib/apt/lists/*

# Copia pacotes Python instalados pelo builder
COPY --from=builder /install /usr/local

# Copia o código da aplicação
COPY . .

# Expõe a porta usada pelo FastAPI (Cloud Run ignora, mas é boa prática)
EXPOSE 8080

# Comando de inicialização em shell form para expandir variável PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
